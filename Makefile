.ONESHELL:
SHELL = /bin/bash

## env : Creates and configures the environment

.PHONY : env
env : 
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml 
	conda activate notebook
	conda install ipykernel
	python -m ipykernel install --user --name make-env --display-name "IPython - Ligo"


## html : build the JupyterBook normally

.PHONY : html
html :
	jupyterbook build .


## clean : clean up the figures, audio and _build folders

.PHONY : clean
clean :
	rm -rf figures/*
	rm -rf audio/*
	rm -rf _build/*

## help : include documentation

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<