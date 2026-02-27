# The-Arctic-Climate

Course project for *Climate and the General Circulation (MO7021)*.

## Overview
This repository contains the material supporting a written report on the Arctic climate system. 
The analysis is based on reanalysis data (2012–2021) and focuses on seasonal variability, large-scale atmospheric circulation, and key surface and atmospheric variables in the Arctic region.

The main emphasis of the project is the written climate analysis. The Python scripts are used to process data and generate the figures included in the report.

## Repository Structure

- `Arctic-project-report/` – LaTeX source files for the written report 
- `PyPlots/` – Generated figures used in the report 
- `readdata.py` – Script for loading and preparing datasets 
- `make_all_figures.py` – Generates all seasonal figures
- `make_map.py` – Arctic map generation (polar stereographic projection)
- `make_relevant_figures.py` – generate figures for report

## Data
The analysis is based on reanalysis datasets. 
Data files are not included in this repository.

## Tools
- Python
- xarray
- matplotlib / cartopy
- cmocean
- LaTeX

## Author
Fredrik Bergelv,
Master’s student in Meteorology, 
MO7021 – Climate and the General Circulation
