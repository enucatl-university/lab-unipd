d = {
    "fbrem_mean_barrel": ["TH1D", ("fbrem_mean_barrel", "fbrem_mean_barrel", 50, 0, 1)],
    "fbrem_mode_barrel": ["TH1D", ("fbrem_mode_barrel", "fbrem_mode_barrel", 50, 0, 1)],
    "p_in_mean_barrel": ["TH1D", ("p_in_mean_barrel", "p_in_mean_barrel", 60, 0, 300)],
    "p_out_mean_barrel": ["TH1D", ("p_out_mean_barrel", "p_out_mean_barrel", 60, 0, 300)],
    "p_in_mode_barrel": ["TH1D", ("p_in_mode_barrel", "p_in_mode_barrel", 60, 0, 300)],
    "p_out_mode_barrel": ["TH1D", ("p_out_mode_barrel", "p_out_mode_barrel", 60, 0, 300)],
    "fbrem_mean_endcap": ["TH1D", ("fbrem_mean_endcap", "fbrem_mean_endcap", 50, 0, 1)],
    "fbrem_mode_endcap": ["TH1D", ("fbrem_mode_endcap", "fbrem_mode_endcap", 50, 0, 1)],
    "p_in_mean_endcap": ["TH1D", ("p_in_mean_endcap", "p_in_mean_endcap", 60, 0, 300)],
    "p_out_mean_endcap": ["TH1D", ("p_out_mean_endcap", "p_out_mean_endcap", 60, 0, 300)],
    "p_in_mode_endcap": ["TH1D", ("p_in_mode_endcap", "p_in_mode_endcap", 60, 0, 300)],
    "p_out_mode_endcap": ["TH1D", ("p_out_mode_endcap", "p_out_mode_endcap", 60, 0, 300)],
    "p_out_mode_endcap": ["TH1D", ("p_out_mode_endcap", "p_out_mode_endcap", 60, 0, 300)],
    "p_out_mode_endcap": ["TH1D", ("p_out_mode_endcap", "p_out_mode_endcap", 60, 0, 300)],
    "p_out_mode_endcap": ["TH1D", ("p_out_mode_endcap", "p_out_mode_endcap", 60, 0, 300)],
    "eta": ["TH1D", ("eta", "eta", 60, -3, 3)],
    "mva_endcap": ["TH1D", ("mva_endcap", "mva_endcap", 40, -0.4, 1)],
    "mva_barrel": ["TH1D", ("mva_barrel", "mva_barrel", 40, -0.4, 1)],
    "chi2ndof_vs_eta": ["TProfile", ("chi2ndof_vs_eta", "chi2ndof_vs_eta", 160, -4, 4)],
    "chi2ndof_vs_fbrem_mode": ["TProfile", ("chi2ndof_vs_fbrem_mode", "chi2ndof_vs_fbrem_mode", 100, 0, 1)],
    }

#only useful because I don't have a fbrem_mean branch in the tree
#and therefore I have to calculate it from p_out_mean and p_in_mean
formula = {
        "eta":"ctf_eta",
    "fbrem_mean_endcap": "1 - p_out_mean / p_in_mean",
    "fbrem_mode_endcap": "fbrem_mode",
    "p_in_mean_endcap": "p_in_mean",
    "p_out_mean_endcap": "p_out_mean",
    "p_in_mode_endcap": "p_in_mode",
    "p_out_mode_endcap": "p_out_mode",
    "fbrem_mean_barrel": "1 - p_out_mean / p_in_mean",
    "fbrem_mode_barrel": "fbrem_mode",
    "p_in_mean_barrel": "p_in_mean",
    "p_out_mean_barrel": "p_out_mean",
    "p_in_mode_barrel": "p_in_mode",
    "p_out_mode_barrel": "p_out_mode",
    "mva_barrel": "mva",
    "mva_endcap": "mva",
    "chi2ndof_vs_eta": "ctf_chi2ndof:ctf_eta",
    "chi2ndof_vs_fbrem_mode": "ctf_chi2ndof:fbrem_mode"
    }

cuts = {
    "fbrem_mean_barrel": "fabs(ctf_eta) < 1.9 && mva > -0.4",
    "fbrem_mode_barrel": "fabs(ctf_eta) < 1.9 && mva > -0.4",
    "fbrem_mean_endcap": "fabs(ctf_eta) > 1.9 && mva > -0.4",
    "fbrem_mode_endcap": "fabs(ctf_eta) > 1.9 && mva > -0.4",
    "p_in_mean_barrel": "fabs(ctf_eta) < 1.9",
    "p_out_mean_barrel": "fabs(ctf_eta) < 1.9",
    "p_in_mode_barrel": "fabs(ctf_eta) < 1.9",
    "p_out_mode_barrel": "fabs(ctf_eta) < 1.9",
    "p_in_mean_endcap": "fabs(ctf_eta) > 1.9",
    "p_out_mean_endcap": "fabs(ctf_eta) > 1.9",
    "p_in_mode_endcap": "fabs(ctf_eta) > 1.9",
    "p_out_mode_endcap": "fabs(ctf_eta) > 1.9",
    "mva_barrel": "fabs(ctf_eta) < 1.9",
    "mva_endcap": "fabs(ctf_eta) > 1.9",
    "chi2ndof_vs_eta": "",
    "chi2ndof_vs_fbrem_mode": "",
    "eta":"",
    }


other_hist_pars = {
    "fbrem_mean_barrel": 
        {"xtitle": "#frac{p_{in} - p_{out}}{p_{in}}",
            "ytitle": "entries / 0.02",
            "logy": True,},
    "fbrem_mode_barrel": 
        {"xtitle": "#frac{p_{in} - p_{out}}{p_{in}}",
            "ytitle": "entries / 0.02",
            "logy": True,},
    "p_in_mean_barrel": 
        {"xtitle": "p_{in} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "p_out_mean_barrel":
        {"xtitle": "p_{out} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "p_in_mode_barrel":
        {"xtitle": "p_{in} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "p_out_mode_barrel":
        {"xtitle": "p_{out} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "fbrem_mean_endcap": 
        {"xtitle": "#frac{p_{in} - p_{out}}{p_{in}}",
            "ytitle": "entries / 0.02",
            "logy": True,},
    "fbrem_mode_endcap": 
        {"xtitle": "#frac{p_{in} - p_{out}}{p_{in}}",
            "ytitle": "entries / 0.02",
            "logy": True,},
    "p_in_mean_endcap": 
        {"xtitle": "p_{in} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "p_out_mean_endcap":
        {"xtitle": "p_{out} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "p_in_mode_endcap":
        {"xtitle": "p_{in} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "p_out_mode_endcap":
        {"xtitle": "p_{out} #[]{Gev / c}",
            "ytitle": "entries / 5 #[]{GeV / c}",
            "logy": True,},
    "chi2ndof_vs_eta":
        {"xtitle": "#eta",
            "ytitle": "#chi^{2}/NDF",
            "logy": True,},
    "chi2ndof_vs_fbrem_mode":
        {"xtitle": "#fbrem_mode",
            "ytitle": "#chi^{2}/NDF",
            "logy": False,},
    "mva_endcap":
        {"xtitle": "mva",
            "ytitle": "entries / 0.02",
            "logy": False,},
    "mva_barrel":
        {"xtitle": "mva",
            "ytitle": "entries / 0.02",
            "logy": False,},
    "eta":
        {"xtitle": "#eta",
            "ytitle": "entries / 0.1",
            "logy": False,},
    }

tree_name = "tree"
colours = [1, 2, 4, 3, 6]
