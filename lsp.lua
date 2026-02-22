-- bootstrap lazy.nvim, LazyVim and your plugins

return {
	{
		"neovim/nvim-lspconfig",
		event = "LazyFile",
		dependencies = {
			{ "mason-org/mason.nvim", version = "2.0.1" },
			{ "mason-org/mason-lspconfig.nvim", version = "2.1.0" },
		},
		opts = {
			diagnostics = {
				underline = true,
				update_in_insert = false,
				virtual_text = true,
				float = {
					focused = false,
					style = "minimal",
					border = "rounded",
					source = "always",
					header = "",
					prefix = "",
				},
			},
			servers = {
				rust_analyzer = {},
				ts_ls = {},
				tailwindcss = {},
				zls = {},
				astro = {},
				denols = {
					settings = {
						deno = {
							lint = true,
							enable = true,
							importMap = "./deno.json",
						},
					},
				},
				mdx_analyzer = {},
				powershell_es = {},
				terraformls = {},
				svelte = {},
				yamlls = {},
				dockerls = {},
				ansiblels = {},
				bashls = {},
				html = {},
				-- htmx = {},
				cssls = {},
				gopls = {},
				ruff = {},
				ty = {},
				docker_compose_language_service = {},
				-- gitlab_ci_ls = {},
				lua_ls = {
					-- cmd = {...},
					-- filetypes = { ...},
					-- capabilities = {},
					settings = {
						Lua = {
							completion = {
								callSnippet = "Replace",
							},
							-- You can toggle below to ignore Lua_LS's noisy `missing-fields` warnings
							-- diagnostics = { disable = { 'missing-fields' } },
						},
					},
				},
			},
		},
		config = function(_, opts)
			-- Setup Mason first
			require("mason").setup()

			-- Setup mason-lspconfig
			local mason_lspconfig = require("mason-lspconfig")
			mason_lspconfig.setup({
				ensure_installed = vim.tbl_keys(opts.servers),
			})

			-- Get lspconfig
			local lspconfig = require("lspconfig")

			-- Setup each server
			for server_name, server_opts in pairs(opts.servers) do
				-- Special handling for conflicting servers
				if server_name == "denols" then
					vim.lsp.config("denols", {
						root_dir = function(bufnr, on_dir)
							if vim.fs.root(bufnr, "deno.json") then
								on_dir(vim.fn.getcwd())
							end
						end,
					})
					vim.lsp.enable("denols")
				elseif server_name == "ts_ls" then
					local check = false
					vim.lsp.config("ts_ls", {
						root_dir = function(bufnr, on_dir)
							if not vim.fs.root(bufnr, "deno.json") then
								if vim.fs.root(bufnr, "package.json") then
									on_dir(vim.fn.getcwd())
								end
								check = true
							end
						end,
					})
					if check then
						vim.lsp.enable("ts_ls")
					end
				else
					lspconfig[server_name].setup(server_opts)
				end
			end
		end,
	},
}
