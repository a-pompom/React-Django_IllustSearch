class IOTest:
    """ ファイルIOが関連するテストのユーティリティクラス """

    TEST_DATA_PATH = 'tests/test_data/'

    def _get_out_file_path(self, out_file_name: str):
        """ 出力されるテストデータのパスを取得

        Returns
        -------
        str
            テストデータの配置されているパス
        """

        return f'{self.TEST_DATA_PATH}{out_file_name}'

    def _setup_for_write(self, in_file_text: str, out_file_name: str):
        """ 前処理 テストデータとして扱う書き込み対象ファイルを作成しておく

        Parameters
        ----------
        in_file_text : str
            ファイル内テキスト文字列
        out_file_name: str
            出力対象ファイル名
        """

        with open (self._get_out_file_path(out_file_name), 'w') as fw:
            fw.write(in_file_text)