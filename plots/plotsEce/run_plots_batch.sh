#!/bin/sh

python make_Control_Plots.py --dl_mt2ll "0,-1"   --dl_mt2bb="0,-1" --dl_mt2blbl="0,-1" --metSig="7,-1" 
python make_Control_Plots.py --dl_mt2ll "100,-1"   --dl_mt2bb="0,-1" --dl_mt2blbl="0,-1"     --metSig="7,-1"  
python make_Control_Plots.py --dl_mt2ll "100,-1"   --dl_mt2bb="70,-1" --dl_mt2blbl="0,-1"    --metSig="7,-1"  
python make_Control_Plots.py --dl_mt2ll "100,-1"   --dl_mt2bb="70,-1" --dl_mt2blbl="100,-1" --metSig="7,-1"  

