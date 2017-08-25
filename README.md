denite-cheatsheet
=================
Cheat sheet source for [denite.nvim](https://github.com/Shougo/denite.nvim)

USAGE
-----
```
Plug 'Shougo/denite.nvim'
Plug 'yuntan/denite-cheatsheet'

" default path for tsv
denite#custom#var('cheatsheet', 'cheatsheet_tsv', '~/.config/nvim/cheatsheet.tsv')
```

Create cheatsheet.tsv and write this:

```
# This is comment
# genre desc mapping command
denite	buffer	<Space>b	Denite buffer
denite	list dotfiles		Denite file_rec:~/.dotfiles/
	edit vimrc		e $MYVIMRC
	reload vimrc		source $MYVIMRC
	setlocal space:2		setlocal shiftwidth=2 tabstop=2 softtabstop=2 expandtab | IndentLinesReset
	setlocal space:4		setlocal shiftwidth=4 tabstop=4 softtabstop=4 expandtab | IndentLinesReset
	setlocal tab:4		setlocal shiftwidth=4 tabstop=4 softtabstop=0 noexpandtab
	reopen with sudo		e sudo:%
	copy file path to clipboard		if has("win32") | let @* = expand("%:p") | else | let @+ = expand("%:p") | endif
	cd to parent directory		execute "cd ".fnameescape(expand("%:p:h"))
	open browser	gx	call feedkeys("gx")
json	prettyfy json		%!python -m json.tool
```

Then run `:Denite cheatsheet`:
[![https://gyazo.com/a82d07b4850216854712a279d9da35ff](https://i.gyazo.com/a82d07b4850216854712a279d9da35ff.png)](https://gyazo.com/a82d07b4850216854712a279d9da35ff)
