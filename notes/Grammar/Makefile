.PHONY: clean all 

NAME = 	pslq

all: $(NAME).pdf
	- pkill -9 evince
	evince $(NAME).pdf &

$(NAME).pdf : $(NAME).tex 
	pdflatex $(NAME).tex
	pdflatex $(NAME).tex
	pdflatex $(NAME).tex

clean:
	rm -f *~ *.aux *.log *.blg *.bbl $(NAME).pdf $(NAME).out
