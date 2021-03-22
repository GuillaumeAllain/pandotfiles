local function replace_units_str (elem)
    local pattern = "(%d+%.?%d*[eE]?[+-]?%d+){(.+)}"

    if FORMAT=='native' then
        elem = pandoc.Str (elem.text:gsub(pattern,"%1 - %2"))
    end

    return elem
end


return {{
    Str = replace_units_str,
}}
