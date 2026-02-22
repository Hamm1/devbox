-- Apply diagnostic config globally after all plugins have loaded
vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    -- Give time for LazyVim and plugins to initialize
    vim.defer_fn(function()
      -- Force diagnostic configuration directly
      vim.diagnostic.config({
        virtual_text = true,
        signs = true,
        underline = true,
        update_in_insert = false,
        severity_sort = true,
        float = {
          focusable = false,
          style = "minimal",
          border = "rounded",
          source = "always",
          header = "",
          prefix = "",
        },
      })
      
      -- Explicitly set up hover diagnostics
      vim.o.updatetime = 250
      vim.cmd([[
        augroup DiagnosticHover
          autocmd!
          autocmd CursorHold * lua vim.diagnostic.open_float(nil, {focus=false})
        augroup END
      ]])
    end, 1000) -- 1 second delay to ensure everything is loaded
  end,
  once = true
})