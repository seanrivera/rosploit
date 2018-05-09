# views.py

import netifaces as ni

from flask import render_template, flash, request
from wtforms import Form, StringField, validators

from demo import demo
from rossploit_scan import scan_node


class ReusableForm(Form):
    target = StringField('Target_IP', validators=[validators.required()])


@demo.route('/', methods=['GET', 'POST'])
def index():
    ip = []
    node_list = []
    form = ReusableForm(request.form)

    if request.method == 'POST' and form.validate():
        # TODO Call rossploit_scan script to scan IP address
        try:
            node_list = scan_node.scan_node(ip_addr=form.target.data, port_range='1-1000',
                                            script_list='ros-node-id.nse')
            flash('Scanned address ' + form.target.data)
            print(node_list)
        except Exception as inst:
            flash("Failed to scan " + form.target.data + " because " + str(inst))

    for iface in ni.interfaces():
        netinfo = ni.ifaddresses(iface)
        if ni.AF_INET in netinfo:
            temp_ip = {'iface': iface, 'addr': netinfo[ni.AF_INET][0]['addr'],
                       'subnet': netinfo[ni.AF_INET][0]['netmask']}
            ip.append(temp_ip)

    return render_template("index.html", ip=ip, form=form, node_list=node_list)


@demo.route('/about')
def about():
    return render_template("about.html")
