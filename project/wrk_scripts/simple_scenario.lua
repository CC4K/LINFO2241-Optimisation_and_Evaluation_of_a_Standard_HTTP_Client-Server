Lorem =
"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer varius dolor sed augue convallis, ac dapibus augue fermentum. Praesent in felis mi. Cras feugiat egestas risus sit amet varius. Etiam dictum magna quis luctus sodales. Etiam pretium varius tortor. Integer ultrices semper quam nec rutrum. Suspendisse lacinia, turpis eu ultrices aliquam, sapien risus iaculis libero, eleifend suscipit tortor urna sit amet libero. Donec vel libero vitae nisi porta dapibus nec sed nibh. Donec mattis risus nunc, aliquet mollis arcu accumsan eget. Suspendisse suscipit nec risus vitae mollis. Quisque bibendum augue eget laoreet faucibus."

function generate_substring(length)
    local input_length = #Lorem -- Get the length of the input string
    -- If the requested length is less than or equal to the input string, return a substring
    if length <= input_length then
        return string.sub(Lorem, 1, length)
    else
        -- Generate a new string by repeating the input string
        local result = Lorem
        while #result < length do
            -- Add characters from the input string until the desired length is reached
            result = result .. string.sub(Lorem, 1, length - #result)
        end
        return result
    end
end

function init(args)
    SizeOfInt = 4

    MatSize = tonumber(os.getenv("matsize"))
    if MatSize == nil then
        print("Error: matsize not found")
        os.exit(1)
    end
    PatternSize = tonumber(os.getenv("patterns_size"))
    if PatternSize == nil then
        print("Error: patterns_size not found")
        os.exit(1)
    end
    NbPattern = tonumber(os.getenv("nb_patterns"))
    if NbPattern == nil then
        print("Error: nb_patterns not found")
        os.exit(1)
    end
    Mat1 = generate_substring(MatSize * MatSize * SizeOfInt)
    Mat2 = generate_substring(MatSize * MatSize * SizeOfInt)
    Patterns = ""
    for i = 1, NbPattern do
        Patterns = Patterns .. generate_substring(PatternSize * SizeOfInt)
    end
end

function request()
    wrk.method = "POST"
    wrk.body = string.format("%d,%d,%d,%s", MatSize, NbPattern, PatternSize, Mat1 .. Mat2 .. Patterns)
    wrk.headers["Content-Type"] = "text/plain"
    return wrk.format()
end
