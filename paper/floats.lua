-- Pandoc Lua filter for the two-column paper (LaTeX output only).
-- 1. Tables: longtable does not work in twocolumn mode, so every table becomes a
--    floating `table` (or `table*` when the caption ends in "[wide]") with a tabular inside.
--    A caption ending in "{#tab:name}" gets \label{tab:name}. Font size: \footnotesize.
-- 2. Figures whose image has the class .wide become figure* (full page width).

local function caption_tex(blocks)
  local tex = pandoc.write(pandoc.Pandoc(blocks), "latex")
  return (tex:gsub("%s+$", ""))
end

function Table(tbl)
  local cap = caption_tex(tbl.caption.long)
  local label, wide = "", false
  cap = cap:gsub("%s*\\{\\#(tab:[%w%-_]+)\\}", function(l) label = "\\label{" .. l .. "}"; return "" end)
  cap = cap:gsub("%s*{#(tab:[%w%-_]+)}", function(l) label = "\\label{" .. l .. "}"; return "" end)
  if pandoc.utils.stringify(tbl.caption.long):find("[wide]", 1, true) then wide = true end
  cap = cap:gsub("%s*{%[}wide{%]}", ""):gsub("%s*%[wide%]", "")
  if tbl.identifier and tbl.identifier ~= "" then label = "\\label{" .. tbl.identifier .. "}" end
  for _, c in ipairs(tbl.classes or {}) do if c == "wide" then wide = true end end
  tbl.caption = pandoc.Caption({})
  tbl.identifier = ""
  tbl.classes = {}
  -- natural column widths (l/r), not the p{} widths pandoc derives from long pipe-table rows
  for i, cs in ipairs(tbl.colspecs) do tbl.colspecs[i] = {cs[1], pandoc.ColWidthDefault} end
  local tex = pandoc.write(pandoc.Pandoc({tbl}), "latex")
  tex = tex:gsub("\\begin{longtable}%[%]", "\\begin{tabular}")
  tex = tex:gsub("\\end{longtable}", "\\bottomrule\n\\end{tabular}")
  tex = tex:gsub("\\bottomrule\\noalign{}\n\\endlastfoot\n", "")
  tex = tex:gsub("\\endfirsthead.-\\endhead\n", "")
  tex = tex:gsub("\\endhead\n", "")
  tex = tex:gsub("\\noalign{}", "")
  -- relative column widths refer to \linewidth (a column or the full page): fine inside the float
  local env = "table"
  local out = "\\begin{" .. env .. "}[tbp]\n\\centering\\footnotesize\\setlength{\\tabcolsep}{3.5pt}\n"
    .. "\\caption{" .. cap .. "}" .. label .. "\n\\fitwidth{" .. tex .. "}" .. "\n\\end{" .. env .. "}"
  return pandoc.RawBlock("latex", out)
end

function Figure(fig)
  local wide = false
  fig:walk({ Image = function(img)
    for _, c in ipairs(img.classes) do if c == "wide" then wide = true end end
  end })
  do return nil end
  local tex = pandoc.write(pandoc.Pandoc({fig}), "latex")
  tex = tex:gsub("\\begin{figure}", "\\begin{figure}[tbp]", 1)
  tex = tex:gsub("\\begin{figure%*}%[tbp%]%[[^%]]*%]", "\\begin{figure*}[tbp]")
  return pandoc.RawBlock("latex", tex)
end
