#! /bin/octave -qf

function word_frequency(input_filename)
    if ~exist(input_filename, 'file')
        error("Input file does not exist: %s", input_filename);
    end

    % Load stop words
    stop_word_filename = "stop_words.txt";
    if exist(stop_word_filename, 'file')
        fid = fopen(stop_word_filename, 'r');
        stop_words_string = fread(fid, '*char')';
        fclose(fid);
        stop_words = strsplit(lower(stop_words_string),',');
        stop_words = strtrim(stop_words); % Remove extra spaces
        stop_words(cellfun('isempty', stop_words)) = []; % Remove empty cells
    else
        error("Not found %s", stop_word_filename);
    end

    % Read input file
    fid = fopen(input_filename, 'r');
    file_contents = fread(fid, '*char')';
    fclose(fid);

    % Convert lower case and tokenize the content
    file_contents = lower(file_contents);
    words = regexp(file_contents, '\w+', 'match');

    % Remove stop words and empty strings
    words = words(~ismember(words, stop_words));
    words(cellfun('isempty', words)) = [];

    % Remove single letters and numbers
    words = words(cellfun(@length, words) > 1);

    % Count the frequency
    [unique_word, ~, ids] = unique(words);
    counts = accumarray(ids, 1);

    % Sort the frequency
    [sorted_counts, sort_indices] = sort(counts, 'descend');
    sorted_words = unique_word(sort_indices);

    for i = 1:min(25, length(sorted_words))
       fprintf('%s - %d\n', sorted_words{i}, sorted_counts(i)); 
    end
end

args = argv();
if numel(argv()) < 1
    error("Please provide an input text file");
else
    word_frequency(argv{1});
end
