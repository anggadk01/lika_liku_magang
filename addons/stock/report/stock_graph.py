# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2008 Tiny SPRL (http://tiny.be) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###############################################################################
from mx.DateTime import *
from pychart import *
import pychart.legend
import time
from report.misc import choice_colors

#
# dRAw a graph for stocks
#
class stock_graph(object):
    def __init__(self, io):
        self._datas = {}
        self._canvas = canvas.init(fname=io, format='pdf')
        self._canvas.set_author("Tiny ERP")
        self._names = {}
        self.val_min = ''
        self.val_max = ''

    def add(self, product_id, product_name, datas):
        if hasattr(product_name, 'replace'):
            product_name=product_name.replace('/', '//')
        if product_id not in self._datas:
            self._datas[product_id] = {}
        self._names[product_id] = product_name
        for (dt,stock) in datas:
            if not dt in self._datas[product_id]:
                self._datas[product_id][dt]=0
            self._datas[product_id][dt]+=stock
            if self.val_min:
                self.val_min = min(self.val_min,dt)
            else:
                self.val_min = dt
            self.val_max = max(self.val_max,dt)

    def draw(self):
        colors = choice_colors(len(self._datas.keys()))
        user_color = {}
        for user in self._datas.keys():
            user_color[user] = colors.pop()

        val_min = int(time.mktime(time.strptime(self.val_min,'%Y-%m-%d')))
        val_max = int(time.mktime(time.strptime(self.val_max,'%Y-%m-%d')))

        plots = []
        for product_id in self._datas:
            f = fill_style.Plain()
            f.bgcolor = user_color[user]
            datas = self._datas[product_id].items()
            datas = map(lambda x: (int(time.mktime(time.strptime(x[0],'%Y-%m-%d'))),x[1]), datas)
            datas.sort()
            datas2 = []
            val = 0
            for d in datas:
                val+=d[1]

                if len(datas2):
                    d2 = d[0]-60*61*24
                    if datas2[-1][0]<d2-1000:
                        datas2.append((d2,datas2[-1][1]))
                datas2.append((d[0],val))
            if len(datas2) and datas2[-1][0]<val_max-100:
                datas2.append((val_max, datas2[-1][1]))
            if len(datas2)==1:
                datas2.append( (datas2[0][0]+100, datas2[0][1]) )
            st = line_style.T()
            st.color = user_color[product_id]
            st.width = 1
            st.cap_style=1
            st.join_style=1
            plot = line_plot.T(label=self._names[product_id], data=datas2, line_style=st)
            plots.append(plot)

        interval = max((val_max-val_min)/15, 86400)
        x_axis = axis.X(format=lambda x:'/a60{}'+time.strftime('%Y-%m-%d',time.gmtime(x)), tic_interval=interval, label=None)
        ar = area.T(size = (620,435), x_range=(val_min,val_max+1), y_axis = axis.Y(format="%d", label="Virtual Stock (Unit)"), x_axis=x_axis)
        for plot in plots:
            ar.add_plot(plot)
        ar.draw(self._canvas)

    def close(self):
        self._canvas.close()

if __name__ == '__main__':
    gt = stock_graph('test.pdf')
    gt.add(1, 'Pomme', [('2005-07-29', 6), ('2005-07-30', -2), ('2005-07-31', 4)])
    gt.add(2, 'Cailloux', [('2005-07-29', 9), ('2005-07-30', -4), ('2005-07-31', 2)])
    gt.draw()
    gt.close()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

