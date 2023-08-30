#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <set>
#include <algorithm>
#include <memory>
#include <sstream>

class tf_execersize {
public:
    virtual std::string get_info() const {
        return typeid(*this).name();
    }
};

class data_storage_manager : public tf_execersize {
    std::vector<std::string> words;

public:
    explicit data_storage_manager(const std::string& path_to_file) {
        std::ifstream file(path_to_file);
        std::string word;
        while (file >> word) {
            word = remove_non_alpha(word);
            if (!word.empty()) {
                words.push_back(to_lowercase(word));
            }
        }
    }

    std::string remove_non_alpha(const std::string& str) {
        std::string result = str;
        result.erase(std::remove_if(result.begin(), result.end(), [](char c){
                    return !std::isalpha(c);
                    
        }), result.end());
        return result;
    }

    std::string to_lowercase(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), ::tolower);
        return result;
    }

    const std::vector<std::string>& get_words() const {
        return words;
    }

    std::string get_info() const override {
        return tf_execersize::get_info() + ": Major data strcture is std::vector";
    }
};

class stop_word_manager : public tf_execersize {
    std::set<std::string> stop_words;

public:
    stop_word_manager() {
        std::ifstream file("./stop_words.txt");
        if (!file.is_open()) {
            std::cerr << "Error: Could not open 'stop_words.txt'." << std::endl;
            exit(1);
        }

        std::string word;
        while (std::getline(file, word, ',')){
            stop_words.insert(word);
        }

        for (char c = 'a'; c<= 'z'; c++){
            stop_words.insert(std::string(1,c));
        }
    }

    bool is_stop_word(const std::string& word) const {
        return stop_words.find(word) != stop_words.end();
    }

    std::string get_info() const override {
        return tf_execersize::get_info() + ": Major structure is std::set";
    }
};

class word_frequency_manager : public tf_execersize {
    std::unordered_map<std::string, int> word_freqs;

public:
    void increment_count(const std::string& word) {
        word_freqs[word]++;
    }

    std::vector<std::pair<std::string, int>> sorted() const {
        std::vector<std::pair<std::string, int>> pairs(word_freqs.begin(), word_freqs.end());
        std::sort(pairs.begin(), pairs.end(), [](const auto& a, const auto& b) {
            return a.second > b.second;
        });
        return pairs;
    }
};

class word_frequency_controller {
    std::unique_ptr<data_storage_manager> data_storage_manager_;
    std::unique_ptr<stop_word_manager> stop_word_manager_;
    std::unique_ptr<word_frequency_manager> word_frequency_manager_;

public:
    explicit word_frequency_controller(const std::string& path_to_file)
        : data_storage_manager_(std::make_unique<data_storage_manager>(path_to_file)),
          stop_word_manager_(std::make_unique<stop_word_manager>()),
          word_frequency_manager_(std::make_unique<word_frequency_manager>()) {}

    void run() {
        for (const auto& word : data_storage_manager_->get_words()) {
            if (!stop_word_manager_->is_stop_word(word)) {
                word_frequency_manager_->increment_count(word);
            }
        }
        int num_words_printed = 0;
        for (const auto& pair : word_frequency_manager_->sorted()) {
            std::cout << pair.first << " - " << pair.second << std::endl;

            num_words_printed++;
            if (num_words_printed >= 25) {
                break;
            }
        }
    }
};

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Pls provide an input file path." << std::endl;
        return 1;
    }

    word_frequency_controller controller(argv[1]);
    controller.run();

    return 0;
}
