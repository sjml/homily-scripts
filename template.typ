// Note that all $variable$ things will get replaced by Pandoc at render-time

#let horizontalrule = line(start: (25%, 0%), end: (75%, 0%))

#let date_string = "$date$"
#let (year, month, day) = date_string.split("-").map(int)
#let date_obj = datetime(
	year: year,
	month: month,
	day: day,
)

#set page(
	paper: "$paper$",
	margin: (x: 1in, top: 1in, bottom: $bottom_margin$),

	header: context {
		set text(size: 12pt)
		let page = counter(page).get().first()

		if page == 1 [
			#align(top)[
				#pad(top: 0.5in)[
					#grid(
						columns: (1fr, auto),
						align(top + left)[#page],
						align(top + right)[
							Lectionary $lectionary_number$: $lectionary_string$ \
							$readings$ \
							$location$; #date_obj.display("[year]-[month repr:short]-[day]")
						],
					)
				]
			]
		] else [
			#align(top)[
				#pad(top: 0.5in)[
					#align(top + left)[#page]
				]
			]
		]
	},
)

#set text(
	font: "$font$",
	lang: "en",
	region: "US",
	size: $font_size$,
)

#v(0.5in) // make room for first-page header

#set par(
	justify: $if(justify)$true$else$false$endif$,
	leading: $leading$,
	spacing: $paragraph_spacing$,
)
#show par: it => block(
	breakable: false,
	inset: (left: 1em, right: 2em),
	it.body
)

$body$
