
local greppattern

local function get_vars (meta)
    if meta.greppattern then
        greppattern = meta.greppattern
    end
end


function get_greppattern_blocks (blocks)

    local body_blocks = {}
    local current_block = {}
    local contains_pattern = false


    for _, block in ipairs(blocks) do
        if block.t == 'Header' and block.level == 1 then
            if contains_pattern then
                for _,v in ipairs(current_block) do
                    table.insert(body_blocks, v)
                end
            end
            if block.content:find(greppattern) then
                contains_pattern = true
            else
                contains_pattern = false
            end
            current_block = {}
            current_block[#current_block+1] = block
        else
            if block.content then
                for _, inlines in ipairs(block.content) do
                    if inlines.text then
                        if inlines.text:find(greppattern) then
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
            table.insert(body_blocks, v)
        end
    end

    -- for _, block in ipairs(blocks) do
    --     if block.t == 'Header' and block.level == 1 then
    --         if block.content[1].text=='TODO' or block.content[1].text=='DONE' then
    --             contains_pattern = true
    --             body_blocks[#body_blocks + 1] = pandoc.Header(block.level, block.content, pandoc.Attr())

    --         elseif contains_pattern and block.level>top_header_level then
    --             body_blocks[#body_blocks + 1] = pandoc.Header(block.level, block.content, pandoc.Attr())
    --         else
    --             contains_pattern = false
    --             top_header_level = 60
    --             -- body_blocks[#body_blocks + 1] = block
    --         end
    --     elseif contains_pattern then
    --         if block.c[1].text=='TODO' or block.c[1].text=='DONE' then
    --             -- print(block.content[2:])
    --             body_blocks[#body_blocks + 1] = pandoc.Header(top_header_level+1, block.content, pandoc.Attr())
    --         else
    --             body_blocks[#body_blocks + 1] = block
    --         end

    --     elseif block.t == 'Para' then
    --         if block.c[1].text=='TODO' or block.c[1].text=='DONE' then
    --             body_blocks[#body_blocks + 1] = pandoc.Header(1, block.content, pandoc.Attr())
    --             -- body_blocks[#body_blocks + 1] = block
    --         end
    --     end
    -- end

    return body_blocks
    -- return blocks
end


return {
    {Meta = get_vars},
    {Blocks = get_greppattern_blocks}
}
