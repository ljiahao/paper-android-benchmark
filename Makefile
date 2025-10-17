PAPERNAME=main
TEXFILES=*.tex *.bib *.sty tex/*.tex
# FIGS=fig/*.pdf

$(PAPERNAME).pdf : $(TEXFILES) $(FIGS) *.bib
	pdflatex $(PAPERNAME)
	bibtex $(PAPERNAME)
	pdflatex $(PAPERNAME)
	pdflatex $(PAPERNAME)
clean:
	rm -f *.ps *.pdf *.dvi *.aux *.log *.blg *~ *.ilg *.idx *.out *.in
