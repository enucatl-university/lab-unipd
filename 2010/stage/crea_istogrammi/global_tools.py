#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

size = 0.045

def set_line(line):
    line.SetLineWidth(2)
    line.SetLineColor(3)
    line.SetLineStyle(2)

def set_gstyle(gStyle):
    gStyle.SetTitleFillColor(0)
    gStyle.SetFillColor(0)
    gStyle.SetStatColor(0)
    gStyle.SetPadColor(0)
    gStyle.SetPadColor(0)

def set_histogram(histogram, x_title, y_title):
    """Set general properties of histogram"""
    histogram.SetLineWidth(2)
    histogram.GetXaxis().SetTitle(x_title)
    histogram.GetYaxis().SetTitle(y_title)
    histogram.GetXaxis().SetDecimals()
    histogram.GetYaxis().SetDecimals()
    histogram.GetXaxis().SetTitleSize(size)
    histogram.GetYaxis().SetTitleSize(size)
    histogram.GetYaxis().SetTitleOffset(1.2)
    histogram.GetXaxis().SetLabelSize(size)
    histogram.GetYaxis().SetLabelSize(size)

def set_canvas(canvas):
    """Set general properties of canvas"""
    canvas.SetFillColor(10)

