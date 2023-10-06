#include <iostream>
#include <fstream>
#include <string>
#include <optional>
#include <algorithm>
#include <cctype>

// Functional style file read
std::optional<std::string> read_file(const std::string& filename){
    std::ifstream file(filename);
    if (!file.is_open()){
        return {}; // Represent failure
    }

    std::string contents;
    file.seekg(0, std::ios::end);
    contents.reserve(file.tellg());
    file.seekg(0, std::ios::beg);

    contents.assign((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    return contents;
}

std::optional<std::string> to_upper(const std::optional<std::string>& input_optional){
    if (!input_optional){
        return {};
    }

    std::string result;
    const auto& input = *input_optional;
    result.reserve(input.size());
    std::transform(input.begin(), input.end(), std::back_inserter(result),
            [](char c) {return std::toupper(static_cast<unsigned char>(c)); });

    return result;
}

int main(int argc, char* argv[]){
    if (argc != 2){
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }

    const auto content = to_upper(read_file(argv[1]));

    if (content) {
        std::cout << *content << std::endl;
    } else {
        std::cout << "Failed to read the file." << std::endl; 
    }

    return 0;
}
