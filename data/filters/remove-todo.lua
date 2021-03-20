function Para (content)
    if content.c[1].text~='TODO' and content.c[1].text~='DONE' then
        return content
    else 
        return {}
    end
end
