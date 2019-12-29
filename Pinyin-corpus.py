import jieba
import pypinyin
import random
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag


def open_readlines(File):
    """打开并按行读取文件"""
    sentences = open('File', 'r', encoding="utf-8")
    sentences = sentences.readlines()
    return sentences


def counter(num):
    """"计数器"""
    if num % 2 == 0:
        print(num)


def intersection(sen1, sen2):
    """求两个字符串的交集"""
    sen1_set = set(sen1)
    sen2_set = set(sen2)
    return ''.join(sen1_set & sen2_set)


def jieba_cut_list(sen):
    """将元句子分割成list类型"""
    sen_list = jieba.cut(sen, cut_all=False)
    sen_str = "" + " ".join(sen_list)
    sen_list = sen_str.split(' ')
    return sen_list


def get_wrong_sen(sen_list):
    """
    生成MWSP类型的错误句子
    不考虑拼音带有ue的汉字
    """
    wrong_sen = ''
    for item in sen_list:
        if is_chinese(item) == True and item != '':
            item_pinyin = get_pinyin(item)
            if 'ue' not in item_pinyin:
                item_pinyin_list = item_pinyin.split()
                item_hanzi = pinyin2Chinese(item_pinyin_list)
                wrong_sen = wrong_sen + ''.join(item_hanzi)
            else:
                wrong_sen = wrong_sen + ''.join(item)
        else:
            wrong_sen = wrong_sen + item
    return wrong_sen


def wrong_sen_tag(sentence, wrong_sentence):
    """错误句子打标签"""
    tags_string = ''
    for i in range(len(sentence)):
        if sentence[i] == wrong_sentence[i]:
            tags_string += 'R'
        else:
            tags_string += 'W'
    return tags_string.strip()


def get_pinyin_tone(word):
    """汉字转拼音（带音调的）"""
    s = ''
    for i in pypinyin.pinyin(word):
        s = s + ''.join(i) + " "
    return s


def get_pinyin(word):
    """汉字转拼音(不带音调的)"""
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i) + ' '
    return s


def pinyin2Chinese(pinyinList, word):
    """拼音转汉字,path_num为推荐的个数"""
    dagParams = DefaultDagParams()
    result = dag(dagParams, pinyinList, log=True)
    num = random.randint(0, len(result) - 1)
    new_word = ''.join(result[num].path)
    if new_word != word:
        return new_word
    else:
        return ''


def get_jieba_cut_list(sen):
    """将原句子分割成list类型"""
    sen_list = jieba.cut(sen, cut_all=False)
    sen_str = "" + " ".join(sen_list)
    sen_list = sen_str.split(' ')
    return sen_list


def is_chinese(unicode_sentence):
    """判断一个unicode是否是汉字"""
    for uchar in unicode_sentence:
        if uchar >= '\u4e00' and uchar <= '\u9fa5':
            continue
        else:
            return False
    else:
        return True



def open_readlines():
    """打开语料数据，一行一行地读"""
    sentences = open('right_sens', 'r', encoding="utf-8")
    sentences = sentences.readlines()
    return sentences


def get_new_sen(sentence):
    """先要将句子中的空格除去，防止出现分词错误
      依次获得拼音和汉字
    """
    if len(sentence) > 9 and len(sentence) < 150:
        sentence = sentence.replace(' ', '')
        sentence = jieba_cut_list(sentence)
        i = random.randint(0, len(sentence) - 1)
        if is_chinese(sentence[i]) and 'ue' not in get_pinyin(sentence[i]):
            word = sentence[i]
            pinyin = get_pinyin(word)
            pinyin = pinyin.split()
            new_word = pinyin2Chinese(pinyin, sentence[i])
            if new_word != '':
                sentence[i] = new_word
                new_sentence = ''.join(sentence)
                return new_sentence.strip()
            else:
                return ''
        else:
            return ''
    else:
        return ''


def get_wrong_str(old, new):
    """获得错误部分的字符串"""
    wrong_str = ''
    for i in range(len(old)):
        if old[i - 1] != new[i - 1]:
            wrong_str = wrong_str + '  ' + '<MISTAKE>' + '\n' + '   ' + '<LOCATION>' + str(
                i) + '</LOCATION>' + '\n' + '    ' + '<WRONG>' + new[
                            i - 1] + '</WRONG>' + '\n' + '    ' + '<CORRECTION>' + old[
                            i - 1] + '</CORRECTION>' + '\n' + '  ' + '</MISTAKE>' + '\n'
    if wrong_str != '':
        return wrong_str


def get_text_str(old):
    text_str = '<SENTENCE>' + '\n' + '  ' + '<TXET>' + '\n' + '    ' + old + '\n' + '  ' + '</TEXT>'
    return text_str


def get_right_form(old, new):
    if len(new) > 1:
        text_str = get_text_str(new)
        wrong_str = get_wrong_str(old, new)
        right_form=text_str+wrong_str.rstrip()+'\n'+'</SENTENCE>'+'\n'+'\n'
        return right_form

def main():
    sentences = open_readlines()
    n=0
    with open('SS-type-sentences', 'w', encoding='utf8') as file_object:
        for sentence in sentences:
            new_sentence = get_new_sen(sentence.strip())
            right_form=get_right_form(sentence.strip(), new_sentence)
            if right_form!= None:
                d=n+1
                n=d
                if n%100==0:
                    print(n)
                file_object.write(right_form)


if __name__ == '__main__':
    main()
