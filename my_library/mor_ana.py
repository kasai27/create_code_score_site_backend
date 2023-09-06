from janome.tokenizer import Tokenizer

# 助詞，助動詞で文章を分割
def split_sentence_by_particles(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    
    result = []
    current_chunk = []
    for token in tokens:
        part_of_speech = token.part_of_speech.split(',')[0]
        if part_of_speech in ['助詞', '助動詞']:
            current_chunk.append(token.surface)
            result.append(''.join(current_chunk))
            current_chunk = []
        else:
            current_chunk.append(token.surface)
    
    if current_chunk:
        result.append(''.join(current_chunk))
    
    return result

# 分かち書きした文字列のコードを抜いた文字数検索
def count_characters_outside_brackets(input_string):
    inside_brackets = False
    count = 0

    for char in input_string:
        if char == '[':
            inside_brackets = True
        elif char == ']':
            inside_brackets = False
        elif not inside_brackets:
            count += 1

    return count

# 分かち書きした文字列をmax_lengthまでの文章に結合
def join_elements_with_limit(lyric_wakati, max_length):
    result = []
    tmp = []
    current_length = 0
    for item in lyric_wakati:

        item_length = count_characters_outside_brackets(item)
        if current_length + item_length <= max_length:
            tmp.append(item)
            current_length += item_length
        else:
            result.append(''.join(tmp))
            tmp = []
            tmp.append(item)
            current_length = 0
            current_length += item_length

    if tmp:
        result.append(''.join(tmp))

    return result


# codeを結合し, 次の分かち文字に結合する関数
def code_join(lyric_split):
    result = []
    brackets_tmp = []
    tmp = []
    flag = False

    for item in lyric_split:

        if item == "[":
            result.append(''.join(tmp))
            tmp = []
            brackets_tmp.append(item)
            flag = True
        elif item == "]":
            brackets_tmp.append(item)
            result.append(''.join(brackets_tmp))
            brackets_tmp = []
            flag = False
        elif flag:
            brackets_tmp.append(item)
        else:
            tmp.append(item)
    if tmp:
        result.append(''.join(tmp))

    return result
