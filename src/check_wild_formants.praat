# process Wilderness only

# replace w/ appropriate 6-digit code
lang$ = "HAUCLV"
tgdir$ = "/Users/eahn/work/outliers/data/wild/annotate/tg/" + lang$ + "_errors_100/"
wavdir$ = "/Users/eahn/work/outliers/data/wild/audio/" + lang$ + "_errors_100/"
outlierfile$ = "/Users/eahn/work/outliers/data/wild/annotate/" + lang$ + "_errors_100.csv"

Read Table from comma-separated file: outlierfile$
Rename: "checkme"
nRows = Get number of rows

for i from 1 to nRows
	selectObject: "Table checkme"
	filename$ = Get value: i, "file"
	start = Get value: i, "start"
	end = Get value: i, "end"
	Read from file: tgdir$ + filename$ + ".TextGrid"
	Read from file: wavdir$ + filename$ + ".wav"
	selectObject: "TextGrid " + filename$
	plusObject: "Sound " + filename$
	View & Edit

	editor: "TextGrid " + filename$
		Zoom: start-0.2, end+0.2
		pauseScript: "check F1 and F2. row " + string$(i) + "/" + string$(nRows)
	endeditor

	# selectObject: "TextGrid " + filename$
	# Save as text file: tgdir$ + filename$ + ".TextGrid"
	select all
	minusObject: "Table checkme"
	Remove
endfor