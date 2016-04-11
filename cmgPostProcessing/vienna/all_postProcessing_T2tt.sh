#!/bin/sh

python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_400to475_mLSP_1to400

python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_100_125_mLSP_1to50
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_150_175_mLSP_1to100
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_200_mLSP_1to125
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_225_mLSP_25to150
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_250_mLSP_1to175
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_275_mLSP_75to200
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_300to375_mLSP_1to300
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_500_525_550_mLSP_1to425_325to450_1to475
python cmgPostProcessing.py --skim=$1 $2 --fastSim --T2tt --samples  SMS_T2tt_mStop_600_950_mLSP_1to450
