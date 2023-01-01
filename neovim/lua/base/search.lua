-- ALIASЫ

local opt = vim.opt --здесь собственно все команды
local g = vim.g --vim global


-- игнор регистров при поиске

opt.ignorecase = true

-- нюанс в виде кэмелкейсов игнорить не будем

opt.smartcase = true

-- подсвечивать что нашлось

opt.showmatch = true
