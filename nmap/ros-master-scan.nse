-- The Head Section --
local http = require "http"
local nmap = require "nmap"
local shortport = require "shortport"
local slaxml = require "slaxml"
local stdnse = require "stdnse"
local strbuf = require "strbuf"
local string = require "string"
local table = require "table"

description = [[
	Performs an XLMPRC lookup of a ROS system. Attempts to call the getSystemState
	to get an idea of the visible nodes and topics. 

	TODO: Eventually it would be wise to additionally scan the ports mentioned as being open and then determine if we can 
	talk to various services running on the robot

	]]

---
-- @args ros-master-scan.url the URI path to request
--
-- @output
-- | Supported Methods:
-- | TODO
-- | TODO
-- |_ TODO
--
-- @xmloutput
-- <table key="Supported Methods">
-- <elem>TODO</elem>
-- <elem TODO</elem>
-- <elem>TODO</elem>
-- <elem TODO</elem>
-- </table>

author = "Sean Rivera"

license = "Same as Nmap--See https://nmap.org/book/man-legal.html"

categories = {
  "discovery",
}

-- The Rule Section --
function portrule (host, port)
  return port.protocol == "tcp" and port.number == 11311 and port.state == "open"
end

--TODO Update this --
local function set_80_columns (t)
  local buffer = strbuf.new()
  for method, description in pairs(t) do
    buffer = (buffer .. string.format("    %s:\n\n", method))
    local line, ll = {}, 0
    local add_word = function (word)
      if #word + ll + 1 < 78 then
        table.insert(line, word)
        ll = ll + #word + 1
      else
        buffer = buffer .. stdnse.strjoin(" ", line) .. "\n"
        ll = #word + 1
        line = {
          word,
        }
      end
    end
    string.gsub(description, "(%S+)", add_word)
    buffer = buffer .. stdnse.strjoin(" ", line) .. "\n\n"
  end
  return "\n" .. strbuf.dump(buffer)
end

local function build_rpc_request (method_name, params_table)
  local retcall = "<methodCall>"
  retcall = retcall .. "<methodName>" .. method_name .. "</methodName>"
  retcall = retcall .. "<params>"
  for ind, param in pairs(params_table) do
    retcall = retcall .. "<param>" .. "<value>"
    retcall = retcall .. "<string>" .. param .. "</string>"
    retcall = retcall .. "</value>" .. "</param>"
  end
  retcall = retcall .. "</params>"
  retcall = retcall .. "</methodCall>"
  return retcall
end


-- The Action Section --
function action (host, port)
  local returns_list = {
    "code",
    "statusMessage",
    "systemState",
  }
  local state_list = {
    "publishers",
    "subscribers",
    "services",
  }
  local recurse_ports = stdnse.get_script_args "ros.follow"
  local url = stdnse.get_script_args(SCRIPT_NAME .. ".url") or "/"
  local caller_id = "/totallyhacker"
  local data = build_rpc_request("getSystemState", {
      caller_id,
    })
  local response = http.post(host, port, url, {
      header = {
        ["Content-Type"] = "application/x-www-form-urlencoded",
      },
    }, nil, data)
  if not (response and response.status and response.body) then
    stdnse.debug1 "HTTP POST failed"
    return nil
  end
  local output = stdnse.output_table()
  output["systemState"] = stdnse.output_table()
  local output_name = "Supported Methods"
  local parser = slaxml.parser:new()
  local under_80 = {
    __tostring = set_80_columns,
  }
  local filter = "<value><string>current system state</string></value>"
  local i_state, v_state = nil, nil
  local output_ptr = output
  local current_pubname = ""
  if response.status == 200 and response.body:find(filter, nil, true) then
    local nest_level = 0
    parser._call = {
      startElement = function (name)
        if name == "array" then
          -- struture of the response [ code, statusMessage, systemState --
          -- structure of the systemState [ publishers, subscribers, services --
          -- structure of the nested publishers [topic [ publisher1, publisher2... ] ] --
          -- structure of the nested subscribers [ topic [subscriber1, subscriber2... ] ] --
          -- structure of the nested services [service [serviceProvider1, serviceProvider2]] --
          nest_level = nest_level + 1
          if nest_level == 1 then
            output["statusMessage"] = output["statusMessage"] or {}
            output_ptr = output["statusMessage"]
          elseif nest_level == 2 then
            output["systemState"] = output["systemState"] or {}
            output_ptr = output["systemState"]
          elseif nest_level == 3 then
            i_state, v_state = next(state_list, i_state)
            output["systemState"][v_state] = output["systemState"][v_state] or {}
            output_ptr = output["systemState"][v_state]
          elseif nest_level == 5 then
            output["systemState"][v_state][current_pubname] = output["systemState"][v_state][current_pubname] or {}
            output_ptr = output["systemState"][v_state][current_pubname]
          end

        end
        parser._call.text = name == "string" and function (content)
          if nest_level == 4 then
            current_pubname = content
          else
            output_ptr = output_ptr or {}
            table.insert(output_ptr, content)
          end
        end
      end,
      closeElement = function (name)
        if name == "array" then
          nest_level = nest_level - 1
        end
        parser._call.text = function ()
          return nil
        end
      end,
    }
    parser:parseSAX(response.body, {
        stripWhitespace = true,
      })
		--TODO: Do I want this? 
    --if recurse_ports then
    --  for ind, val in pairs(state_list) do
    --    print("Beginning to recurse on all found " .. val .. " now\n")
    --    for ind2, val2 in pairs(output["systemState"][val]) do
    --      if val == "publishers" or val == "subscribers" then
    --        data = build_rpc_request("lookupNode", {
    --            caller_id,
    --            ind2,
    --          })
    --      else
    --        data = build_rpc_request("lookupService", {
    --            caller_id,
    --            ind2,
    --          })
    --      end
    --      --TODO: Function this
    --      local response_nest = http.post(host, port, url, {
    --          header = {
    --            ["Content-Type"] = "application/x-www-form-urlencoded",
    --          },
    --        }, nil, data)
    --      if not (response_nest and response_nest.status and response_nest.body) then
    --        stdnse.debug1 "HTTP POST FAILED "
    --        --stdnse.debug1 "HTTP POST FAILED for type " .. val .. " and topic " .. ind2
    --        return nil
    --      end
    --      print(response_nest.body)
    --    end
    --  end
    --end
    return output
  elseif response.body:find("<name>faultCode</name>", nil, true) then
    output.error = "XMLRPC instance doesn't support introspection."
    return response.body
    --return output, output.error
  end
end
