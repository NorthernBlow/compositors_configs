local plugins = {
  {
    "mfussenegger/nvim-dap",
  },
  {
    "mfussenegger/nvim-dap-python",
    ft = "python",
    dependencies = {
      "mfussenegger/nvim-dap",
    },
    config = function (_, opts)
      local path = "~/.local/share/nvim/mason/packages/debugpy/venv/bin/python"
      require("dap-python").setup(path)
    end,
  },
  {
    "jose-elias-alvarez/null-ls.nvim",
    ft = {"python"},
    opts = function ()
      return require "custom.configs.null-ls"
      
    end,
  },
  {
  "williamboman/mason.nvim",
  opts = {
    ensure_installed = {
      "black",
      "debugpy",
      "mypy",
      "ruff",
      "pyright",
    },
  },
},
  {
    "neovim/nvim-lspconfig",
    config = function ()

      require "plugins.configs.lspconfig"
      require "custom.configs.lspconfig"
    end,
  },
}



return plugins
