# 多层基金持仓的气候暴露穿透与覆盖诊断资料工具

这个 Python 项目保存业务记录及其披露修订，提供现有直接计算和资料诊断。样本为虚构资料，仅用于核对字段与现有计算，不代表真实机构的经营或排放情况。

## 文件与运行

- financed/records.py：不可变资料副本、修订选择和指纹。
- financed/model.py：领域实体与输入约束。
- financed/operations.py：已有直接计算，具体行为见下节。
- data/sample.json：可直接读取的业务样本。

Python 3.11 或更新版本即可，不依赖第三方包。已有测试与编译检查：

```sh
python -m unittest discover -s tests -v
python -m compileall -q financed
python -m financed data/sample.json --as-of 2026-11-15T00:00:00Z
```

## 已有行为

直接持仓估值、基金成分覆盖率及直接环边保留。不进行多层基金穿透，也不将未披露成分视作现金。

## 记录约定

每条记录有 kind、id、revision、known_at 与 data。kind 和 id 共同标识同一个逻辑记录，revision 是正整数。以 known_at 不晚于指定时点的最新修订为准，披露时点相同则选择更大 revision。deleted 标记撤回当前记录，不能恢复成更早修订。所有记录正文保留在输入中，读视图不改写源资料。金额、用量和因子使用十进制文本，RecordBook 只负责资料身份与时点筛选，领域约束由对应模块核对。

领域单位与兼容语义见 [CONTRACT.md](CONTRACT.md)。
