\documentclass[italian,a4paper]{article}
\usepackage[tight,nice]{units} %unità di misura
\usepackage{babel,amsmath,amssymb,amsthm,graphicx,url}
\usepackage[text={5.5in,9in},centering]{geometry}
\usepackage[utf8x]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{ae,aecompl}
\usepackage{pstricks}
\usepackage[footnotesize,bf]{caption}
\usepackage{textcomp}
\usepackage{gensymb}
\frenchspacing
\pagestyle{plain}
%------------- eliminare prime e ultime linee isolate
\clubpenalty=9999%
\widowpenalty=9999
%--- definizione numerazioni
\renewcommand{\theequation}{\thesection.\arabic{equation}}
\renewcommand{\thefigure}{\arabic{figure}}
\renewcommand{\thetable}{\arabic{table}}
\addto\captionsitalian{\renewcommand{\figurename}{Grafico}}
%
%------------- ridefinizione simbolo per elenchi puntati: en dash
%\renewcommand{\labelitemi}{\textbf{--}}
\renewcommand{\labelenumi}{\textbf{\arabic{enumi}.}}
\setlength{\abovecaptionskip}{\baselineskip}   % 0.5cm as an example
\setlength{\floatsep}{2\baselineskip}
\setlength{\belowcaptionskip}{\baselineskip}   % 0.5cm as an example
%--------- comandi insiemi numeri complessi, naturali, reali e altre abbreviazioni
\renewcommand{\leq}{\leqslant}
%--------- porzione dedicata ai float in una pagina:
\renewcommand{\textfraction}{0.05}
\renewcommand{\topfraction}{0.95}
\renewcommand{\bottomfraction}{0.95}
\renewcommand{\floatpagefraction}{0.35}
\setcounter{totalnumber}{5}
%---------
%
%---------
\begin{document}
\title{Relazione di laboratorio: transistor}
\author{\normalsize Ilaria Brivio (582116)\\%
\normalsize \url{brivio.ilaria@tiscali.it}%
\and %
\normalsize Matteo Abis (584206)\\ %
\normalsize \url{webmaster@latinblog.org}
\and %
\normalsize Lorenzo Rossato (579393)\\ %
\normalsize \url{supergiovane05@hotmail.com}}
\date{\today}
\maketitle
%------------------
\section{Metodologia di misura}
Abbiamo immesso in $V_{\text{in}}$ un segnale in onda quadra con \unit[5]{V} pp,
valore medio \unit[2.5]{V} e frequenza \unit[10.40]{kHz}. Il valore nominale
della resistenza $R_{\text{c}}$ vale
\unit[$1$]{k\ohm}e per la resistenza $R_{\text{b}}$ vale \unit[330]{k\ohm}.
Abbiamo collegato $V_{\text{in}}$ e $V_{\text{out}}$ ai canali 1 e 2 dell'oscilloscopio
rispettivamente, mediante le sonde precedentemente compensate.
L'andamento
dell'ingresso e dell'uscita in funzione del tempo per la durata di un
periodo è riportato in figura~\ref{fig:vinvout}.
\begin{figure}[h]\caption{Rappresentazione schematica del circuito
    realizzato}
    \centering
    \include{circuito}
\end{figure}
Al segnale in $V_{\text{out}}$ corrisponde un valore di
$\Delta V = \unit[4.48]{V}$. Definito il tempo di salita di un segnale il tempo
 impiegato per passare dal $10 %$ al $90 %$ del suo valore finale 
(ugualmente per la discesa), abbiamo $10 \% \Delta V = \unit[0.45]{V}$ e $90\% \Delta V = \unit[4.03]{V}$ a cui corrisponde una differenza di tempo di: 

\begin{table}[h]
    \centering
    \begin{tabular}{*4c}
 {}     &  t                 &  $ V div $      & T div\\\hline
\multicolumn{4}{c}
salita  & \unit[1740]{\mu s} & \unit[780] {mV} & \unit[500]{ns}\\\hline
 
\multicolumn{4}{c}{scala t = \unit[500]{ns}, V = \unit[1]{V}}\\
discesa & \unit[2720]{\mu s} & \unit[1]{V}     & \unit[500]{ns}\\\hline

\end{tabular}
\end{table}
\newpage

Si vuole ora calcolare il valore minimo della resistenza di collettore che manda il transistor in saturazione, ovvero quando $V_[{\text{out}}$ raggiunge il valore di circa \unit[0.2]{V}.
Abbiamo $I_{\text{c}}= \beta I_{\text{b}}= 350 \dot \unit[13]{\mu A}= \unit[4.7]{mA} $; dall'equazione 
$V_{\text{ce}}V_{\text{c}} - I_{\text{c}}R = 0.2$ si ottiene esplicitando la resistenza $R = \dfrac{14.8}{4.7}= \unit[3.15]{k\ohm}$
a fronte di un valore misurato di $R =\unit[3.3]{k\ohm} $ e $V_{\text{ce}}= \unit[0.192]{V}$.


\begin{figure}[h]\caption{Andamento di $V_{\text{in}}$ e $V_{\text{out}}$ (\unit{V}) in funzione del tempo (\unit{ms}).}
        \centering                                     
        \include{andamento}
    \label{fig:vinvout}
\end{figure}
\end{document}
