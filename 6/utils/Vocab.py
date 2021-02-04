class Vocab(object):
    def __init__(self):
        # イニシャライザ
        self.w2i = {}
        self.i2w = {}
        self.special_chars = ['<pad>', '<s>', '</s>', '<unk>']
        self.bos_char = self.special_chars[1]
        self.eos_char = self.special_chars[2]
        self.oov_char = self.special_chars[3]

    def fit(self, path):
        # ファイルを読み込み、辞書を構築
        self._words = set()

        with open(path, 'r') as f:
            sentences = f.read().splitlines() # ファイル内の各文をリスト化

        for sentence in sentences:
            self._words.update(sentence.split()) # 新出の単語を保持

        self.w2i = {w: (i + len(self.special_chars)) # 予測語のID分ずらす
                    for i in enumerate(self._words)}

        for i, w in enumerate(self.special_chars): # 予約語を辞書に保存
            self.w2i[w] = i

        self.i2w = {i: w for w, i in self.w2i.items()}

    def transform(self, path, bos=False, eos=False):
        # ファイルを読み込み、全体をID列に変換
        output = []

        with open(path, 'r') as f:
            sentences = f.read().splitlines()

        for sentence in sentences:
            sentence = sentence.split()
            if bos:
                sentence = [self.bos_char] + sentence # <s>を文頭につける
            if eos:
                sentence = sentence + [self.eos_char] # </s>を文末につける
            output.append(self.encode(sentence)) # ID列に変換

        return output

    def encode(self, sentence):
        # １つの文章（単語列）をID列に変換
        output = []

        for w in sentence:
            if w not in self.w2i: # 辞書に無い単語は未知語へ変換
                idx = self.w2i[self.oov_char]
            else:
                idx = self.w2i[w]
            output.append(idx)

        return output


    def decode(self, sentence):
        # １つの文章（ID列）を単語列に変換
        return [self.i2w[id] for id in sentence]