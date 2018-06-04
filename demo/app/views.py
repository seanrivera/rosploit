# views.py

import netifaces as ni
from typing import List

from flask import render_template, flash, session, request
from wtforms import Form, StringField, validators

import rosploit
from demo import demo
from rosploit import node_scripts
from rosploit.node import Node
from rosploit_scan import scan_node


class ReusableForm(Form):
    target = StringField('Target_IP', validators=[validators.required()])


@demo.route('/', methods=['GET', 'POST'])
def index():
    ip = []
    node_list: List[Node] = []
    if 'scan_results' not in session:
        session['scan_results'] = {}
    node_dict = session['scan_results']
    form = ReusableForm(request.form)

    if request.method == 'POST':
        if 'submit' in request.form and form.validate() and form.target.data:
            # TODO Call rosploit_scan script to scan IP address
            ip_addr: str = form.target.data.strip()
            try:
                temp_list = scan_node.scan_node(ip_addr=ip_addr, port_range='10000-',
                                                script_list=['ros-node-id.nse', 'ros-master-scan.nse'])
                node_dict[ip_addr] = [x.toJSON() for x in temp_list]
                flash('Scanned address ' + ip_addr)
            except Exception as inst:
                flash("Failed to scan " + ip_addr + " because " + str(inst))
                raise inst

        elif 'action' in request.form:
            print(request.form['action'])
            print(request.form['node'])
            # TODO: this is agressively inefficient
            action = getattr(rosploit, request.form['action'])
            action_node = Node.fromJSON(request.form['node'])
            result = action(action_node)
            flash(result)

    try:
        for item in node_dict.values():
            node_list.extend([Node.fromJSON(x) for x in item])
    except Exception as inst:
        flash('Had an exception making the node list! ' + inst)
    scripts = node_scripts
    for iface in ni.interfaces():
        netinfo = ni.ifaddresses(iface)
        if ni.AF_INET in netinfo:
            temp_ip = {'iface': iface, 'addr': netinfo[ni.AF_INET][0]['addr'],
                       'subnet': netinfo[ni.AF_INET][0]['netmask']}
            ip.append(temp_ip)
    session['scan_results'] = node_dict
    return render_template("index.html", ip=ip, form=form, node_list=node_list, scripts=scripts)


@demo.route('/about')
def about():
    return render_template("about.html")
