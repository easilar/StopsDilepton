nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=allZ --mode=doubleMu > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=allZ --mode=doubleEle > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=onZ --mode=doubleMu > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=onZ --mode=doubleEle > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=offZ --mode=doubleEle > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=offZ --mode=doubleMu > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=allZ --mode=muEle > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=onZ --mode=muEle > output.log" &
nohup krenew -t -K 10 -- bash -c "python simple1DPlots.py $1 --zMode=offZ --mode=muEle > output.log" &
