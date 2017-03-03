分別在input images、model variables、feature maps加上error

1.input images:  making_error.py
function addError() 的用途是在一張32*32的圖片以bit為單位隨機加error，其中function square()可幫助定義內部外部範圍。
function main()中 err_rate可控制error rate，加完error後存回test_batch.bin，呼叫cifar10_eval計算準確率，並依序存進csv檔中。
function show() 可顯示圖片，幫助確認error結果。
note: 原始的test_batch.bin會被改動，若之後要進行其他實驗要注意是不是原來的檔案。

2.model variables: cifar10_eval_modelError.py
以原本的cifar10_eval為底更改，error用gaussian noise模擬，更動的部分有註解並標註"cyshen"
scope 跟 var 指的是要在哪個scope下的哪個variable加error
noise的shape要隨著不同variable改變，variable的詳細資訊可以用tensorflow library "inspect_checkpoint"確認，以下是網址:https://www.tensorflow.org/versions/r0.10/how_tos/variables/index.html
最後結果一樣存成csv檔，檔名是variable名稱。

3.feature maps: cifar10_eval_featureError.py
但主要的更動其實在cifar10_featureError.py，更動的地方一樣有註解，要注意儲存csv的檔名要手動改。