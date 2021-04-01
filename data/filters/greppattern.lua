local function get_greppattern_pandoc( doc )
    local body_blocks={}
    local current_block = {}
    local contains_pattern = false

    if doc.meta.greppattern then
        for _, block in ipairs(doc.blocks) do
            if block.t == 'Header' and block.level == 1 then
                if contains_pattern then
                    for _,v in ipairs(current_block) do
                        -- table.insert(body_blocks, v)
                        body_blocks[#body_blocks+1] = v
                    end
                end
                for _, inlines in ipairs(block.content) do
                    if inlines.text then
                        if inlines.text:find(doc.meta.greppattern) then
                            contains_pattern = true
                        end
                    end
                end
                current_block = {}
                current_block[#current_block+1] = block
            else
                if block.content then
                    for _, inlines in ipairs(block.content) do
                        if inlines.text then
                            if inlines.text:find(doc.meta.greppattern) then
                                contains_pattern = true
                            end
                        end
                    end
                end
                current_block[#current_block+1] = block
            end
        end

        if contains_pattern then
            for _,v in ipairs(current_block) do
                body_blocks[#body_blocks+1] = v
            end
        end
    else
        body_blocks = doc.blocks
    end
    return pandoc.Pandoc(body_blocks, doc.meta)
end

return {
    {Pandoc = get_greppattern_pandoc}
}
