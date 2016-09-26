import os

runOnGentT2 = True

if os.environ['USER'] in ['schoef', 'rschoefbeck', 'schoefbeck']:
    # Where you store cmg output
    cmg_directory      = "/scratch/rschoefbeck/cmgTuples/80X_1l_9"
    # Where postprocessed data goes 
    data_output_directory      = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    #data_output_directory      = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    # Where you store the data
    data_directory      = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    # Where the plots go
    plot_directory      = "/afs/hephy.at/user/r/rschoefbeck/www/"
    # Analysis result files
    analysis_results    = '/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/80X_v12' #Path to analysis results
    # directory with veto lists
    veto_lists = "/afs/hephy.at/data/rschoefbeck01/StopsDilepton/vetoLists/"
    # 715 release for limit calculation 
    combineReleaseLocation = '/afs/hephy.at/work/r/rschoefbeck/CMS/tmp/CMSSW_7_1_5/src'
    runOnGentT2 = False

if os.environ['USER'] in ['easilar']:
    # Where you store cmg output (chunks)
    cmg_directory      = "/scratch/rschoefbeck/cmgTuples/80X_1l_9"
    # Where postprocessed data goes 
    data_output_directory      = "/afs/hephy.at/data/easilar/cmgTuples/"
    # Where you store the data (postporcessed)
    data_directory      = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    # Where the plots go
    plot_directory      = "/afs/hephy.at/user/e/easilar/www/"
    # Analysis result files
    analysis_results    = '/afs/hephy.at/data/easilar01/StopsDilepton/results'
    # directory with veto lists
    veto_lists = "/afs/hephy.at/data/rschoefbeck01/StopsDilepton/vetoLists/"
    # 715 release for limit calculation 
    combineReleaseLocation = '/afs/hephy.at/work/r/rschoefbeck/CMS/tmp/CMSSW_7_1_5/src'
    runOnGentT2 = False

if os.environ['USER'] in ['tomc']:
    # Where you store cmg output
    cmg_directory              = "/pnfs/iihe/cms/store/user/tomc/cmgTuples/80X_v6"
    # Where postprocessed data goes 
    data_output_directory      = "/user/tomc/StopsDilepton/data"
    # Where you store the data for plotting, analysis etc.
    data_directory             = "/user/tomc/StopsDilepton/data"
    # Where the plots go
    plot_directory             = "/user/tomc/StopsDilepton/plots_80X_v13"
    # Analysis result files
    analysis_results           = "/user/tomc/StopsDilepton/results_80X_v13"
    # Release for limit calculation (seems the 74X release is now also recommended for users)
    combineReleaseLocation     = '/user/tomc/StopsDilepton/CMSSW_7_4_7/src/'
