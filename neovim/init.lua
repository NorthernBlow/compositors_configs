-- line numbers by default
vim.wo.number = true

local lazypath = vim.fn.stdpath 'data' .. '/lazy/lazy.nvim'
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system { 'git', 'clone', '--filter=blob:none', 'https://github.com/folke/lazy.nvim.git', '--branch=stable', lazypath }
end
vim.opt.rtp:prepend(lazypath)


-- Add plugin
require('lazy').setup({
	'nvim-lualine/lualine.nvim',
	'nvim-treesitter/nvim-treesitter',
	'nvim-treesitter/nvim-treesitter-textobjects',
	'neovim/nvim-lspconfig',
	'williamboman/mason.nvim',
	'williamboman/mason-lspconfig.nvim',
	'WhoIsSethDaniel/mason-tool-installer.nvim',
	

}, {})

--Set statusbar
require('lualine').setup {
  options = {
    icons_enabled = false,
    theme = 'onedark',
    component_separators = '|',
    section_separators = '',
  },
}


local M = {}

function M.setup(servers, options)
  local lspconfig = require "lspconfig"
  local icons = require "config.icons"
end



require("mason-lspconfig").setup {
    ensure_installed = vim.tbl_keys(servers),
    automatic_installation = false,
  }



--set mason plugin manager
require("mason").setup({
    ui = {
        icons = {
            package_installed = "✓",
            package_pending = "➜",
            package_uninstalled = "✗"
        }
    }
})

--force mason to install needed plugins ><
require("mason-tool-installer").setup {
  ensure_installed = { "stylua", "prettierd", "pyright" },
  auto_update = true,
  run_on_start = true,
}
