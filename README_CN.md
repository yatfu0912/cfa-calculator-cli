# CFA 计算器命令行工具

一个轻量级、快速且用户友好的 CFA（特许金融分析师）金融计算命令行工具。

## 功能特性

- **货币时间价值 (TVM)**: 终值、现值、年金、永续年金、有效年利率
- **投资组合管理**: 夏普比率、特雷诺比率、詹森阿尔法、贝塔系数、CAPM、索提诺比率
- **固定收益**: 债券价格、到期收益率、赎回收益率、当前收益率、麦考利久期、修正久期、凸性
- **股权估值**: DDM、FCFE、市盈率估值（即将推出）
- **衍生品**: Black-Scholes、期权定价（即将推出）
- **统计学**: 均值、标准差、相关性、协方差（即将推出）

## 安装

### 系统要求

- Python 3.10 或更高版本
- pip

### 从源码安装

```bash
cd "Calculator CLI"
pip install -e .
```

这将全局安装 `cfa` 命令。

## 使用指南

### 查看帮助

```bash
cfa --help              # 查看主帮助
cfa tvm --help          # 查看货币时间价值模块帮助
cfa portfolio --help    # 查看投资组合管理模块帮助
```

### 货币时间价值 (TVM) 示例

#### 1. 计算终值 (Future Value)

```bash
cfa tvm fv --pv 1000 --rate 0.05 --n 10
```
**说明**: 计算 $1,000 在 5% 年利率下 10 年后的终值  
**结果**: 约 $1,628.89

**参数说明**:
- `--pv`: 现值 (Present Value)
- `--rate`: 年利率（小数形式，如 0.05 表示 5%）
- `--n`: 年数
- `--freq`: 复利频率（可选，默认为 1）
  - 1 = 年复利
  - 2 = 半年复利
  - 4 = 季度复利
  - 12 = 月复利

**示例 - 半年复利**:
```bash
cfa tvm fv --pv 1000 --rate 0.08 --n 5 --freq 2
```

#### 2. 计算现值 (Present Value)

```bash
cfa tvm pv --fv 15000 --rate 0.06 --n 10
```
**说明**: 计算 10 年后的 $15,000 在 6% 折现率下的现值

#### 3. 计算年金 (Annuity)

**普通年金现值**:
```bash
cfa tvm annuity --pmt 1000 --rate 0.05 --n 20 --type pv --annuity-type ordinary
```
**说明**: 计算每期支付 $1,000，共 20 期，利率 5% 的普通年金现值

**即付年金终值**:
```bash
cfa tvm annuity --pmt 1000 --rate 0.05 --n 20 --type fv --annuity-type due
```
**说明**: 计算期初支付的年金终值

**参数说明**:
- `--pmt`: 每期支付金额
- `--rate`: 每期利率
- `--n`: 期数
- `--type`: 计算类型（`pv` = 现值，`fv` = 终值）
- `--annuity-type`: 年金类型（`ordinary` = 普通年金/期末支付，`due` = 即付年金/期初支付）

#### 4. 计算永续年金 (Perpetuity)

**普通永续年金**:
```bash
cfa tvm perpetuity --pmt 100 --rate 0.05
```
**说明**: 计算每年支付 $100 的永续年金现值  
**结果**: $2,000

**增长型永续年金**:
```bash
cfa tvm perpetuity --pmt 100 --rate 0.08 --growth 0.03
```
**说明**: 计算初始支付 $100，每年增长 3%，折现率 8% 的永续年金现值

#### 5. 计算有效年利率 (EAR)

```bash
cfa tvm ear --stated-rate 0.08 --freq 2
```
**说明**: 计算名义年利率 8%，半年复利的有效年利率  
**结果**: 约 8.16%

### 投资组合管理 (Portfolio) 示例

#### 1. 夏普比率 (Sharpe Ratio)

```bash
cfa portfolio sharpe --return 0.12 --rf 0.03 --std 0.15
```
**说明**: 计算投资组合的夏普比率  
**结果**: 0.60

**参数说明**:
- `--return`: 投资组合收益率（小数形式）
- `--rf`: 无风险利率
- `--std`: 投资组合标准差

**解读**: 夏普比率越高，表示风险调整后的收益越好

#### 2. 特雷诺比率 (Treynor Ratio)

```bash
cfa portfolio treynor --return 0.15 --rf 0.03 --beta 1.2
```
**说明**: 计算特雷诺比率，衡量每单位系统风险的超额收益

#### 3. 詹森阿尔法 (Jensen's Alpha)

```bash
cfa portfolio alpha --return 0.15 --rf 0.03 --beta 1.2 --market-return 0.11
```
**说明**: 计算詹森阿尔法，衡量相对于 CAPM 的超额收益

**参数说明**:
- `--return`: 实际投资组合收益率
- `--rf`: 无风险利率
- `--beta`: 投资组合贝塔系数
- `--market-return`: 市场收益率

**解读**: 正的阿尔法值表示跑赢市场

#### 4. 索提诺比率 (Sortino Ratio)

```bash
cfa portfolio sortino --return 0.12 --target 0.03 --downside-std 0.10
```
**说明**: 类似夏普比率，但只惩罚下行波动

#### 5. 贝塔系数 (Beta)

```bash
cfa portfolio beta --asset-returns "0.10,0.15,0.12,0.08,0.14" --market-returns "0.08,0.12,0.10,0.06,0.11"
```
**说明**: 根据历史收益率数据计算贝塔系数

**参数说明**:
- `--asset-returns`: 资产收益率序列（逗号分隔）
- `--market-returns`: 市场收益率序列（逗号分隔）

**解读**:
- β > 1: 比市场波动更大
- β < 1: 比市场波动更小
- β = 1: 与市场波动相同

#### 6. CAPM 必要收益率

```bash
cfa portfolio capm --rf 0.03 --beta 1.2 --market-return 0.11
```
**说明**: 使用资本资产定价模型计算必要收益率  
**公式**: E(Ri) = Rf + β × [E(Rm) - Rf]  
**结果**: 12.6%

#### 7. 投资组合预期收益率

```bash
cfa portfolio portfolio-return --weights "0.6,0.4" --returns "0.10,0.15"
```
**说明**: 计算投资组合的预期收益率

**参数说明**:
- `--weights`: 各资产权重（必须加总为 1）
- `--returns`: 各资产预期收益率

#### 8. 协方差和相关系数

```bash
cfa portfolio covariance --returns1 "0.10,0.12,0.14" --returns2 "0.08,0.10,0.12"
```
**说明**: 计算两个资产之间的协方差和相关系数

### 固定收益 (Bond) 示例

#### 1. 计算债券价格 (Bond Price)

```bash
cfa bond price --face 1000 --coupon-rate 0.06 --ytm 0.055 --years 8 --freq 2
```
**说明**: 计算面值 $1,000，票面利率 6%，到期收益率 5.5%，8 年到期的债券价格  
**结果**: 约 $1,032.01（溢价债券）

**参数说明**:
- `--face`: 面值/票面价值
- `--coupon-rate`: 年票面利率（小数形式）
- `--ytm`: 到期收益率（年化，小数形式）
- `--years`: 到期年限
- `--freq`: 付息频率（2 = 半年付息）

**解读**: 价格 > 面值 = 溢价债券；价格 < 面值 = 折价债券

#### 2. 计算到期收益率 (YTM)

```bash
cfa bond ytm --price 1050 --face 1000 --coupon-rate 0.06 --years 5 --freq 2
```
**说明**: 计算当前价格 $1,050 的债券的到期收益率  
**结果**: 约 4.86%

**解读**: YTM 是持有至到期的内部收益率

#### 3. 计算久期 (Duration)

```bash
cfa bond duration --face 1000 --coupon-rate 0.05 --ytm 0.06 --years 10 --freq 2
```
**说明**: 计算麦考利久期和修正久期  
**结果**: 
- 麦考利久期: 约 7.90 年
- 修正久期: 约 7.67

**解读**: 修正久期衡量债券价格对收益率变化的敏感度

#### 4. 计算凸性 (Convexity)

```bash
cfa bond convexity --face 1000 --coupon-rate 0.06 --ytm 0.06 --years 10 --freq 2
```
**说明**: 计算凸性，衡量价格-收益率关系的曲率

**解读**: 凸性越高，债券价格对利率变化的反应越非线性

#### 5. 计算赎回收益率 (YTC)

```bash
cfa bond ytc --price 1050 --face 1000 --coupon-rate 0.08 --years-to-call 5 --call-price 1030 --freq 2
```
**说明**: 计算可赎回债券在最早赎回日被赎回的收益率

**参数说明**:
- `--years-to-call`: 距离赎回日的年数
- `--call-price`: 赎回价格

#### 6. 计算当前收益率 (Current Yield)

```bash
cfa bond current-yield --price 1050 --face 1000 --coupon-rate 0.06
```
**说明**: 计算当前收益率（年票息 / 当前价格）  
**结果**: 约 5.71%

**解读**: 当前收益率不考虑资本利得/损失

### 使用 --explain 标志

在任何命令后添加 `--explain` 可以显示计算公式：

```bash
cfa tvm fv --pv 1000 --rate 0.05 --n 10 --explain
```
**输出**: 显示公式 FV = PV × (1 + r/freq)^(n×freq)

```bash
cfa bond duration --face 1000 --coupon-rate 0.05 --ytm 0.06 --years 10 --freq 2 --explain
```
**输出**: 显示公式 ModDur = MacDur / (1 + YTM/freq)

## 命令参考

### 货币时间价值 (tvm)

| 命令 | 说明 | 主要参数 |
|------|------|----------|
| `fv` | 终值 | `--pv`, `--rate`, `--n`, `--freq` |
| `pv` | 现值 | `--fv`, `--rate`, `--n`, `--freq` |
| `annuity` | 年金终值/现值 | `--pmt`, `--rate`, `--n`, `--type`, `--annuity-type` |
| `perpetuity` | 永续年金现值 | `--pmt`, `--rate`, `--growth`（可选） |
| `ear` | 有效年利率 | `--stated-rate`, `--freq` |

### 投资组合管理 (portfolio)

| 命令 | 说明 | 主要参数 |
|------|------|----------|
| `sharpe` | 夏普比率 | `--return`, `--rf`, `--std` |
| `treynor` | 特雷诺比率 | `--return`, `--rf`, `--beta` |
| `alpha` | 詹森阿尔法 | `--return`, `--rf`, `--beta`, `--market-return` |
| `sortino` | 索提诺比率 | `--return`, `--target`, `--downside-std` |
| `beta` | 贝塔系数 | `--asset-returns`, `--market-returns` |
| `capm` | CAPM 必要收益率 | `--rf`, `--beta`, `--market-return` |
| `portfolio-return` | 投资组合收益率 | `--weights`, `--returns` |
| `covariance` | 协方差和相关系数 | `--returns1`, `--returns2` |

### 固定收益 (bond)

| 命令 | 说明 | 主要参数 |
|------|------|----------|
| `price` | 债券价格 | `--face`, `--coupon-rate`, `--ytm`, `--years`, `--freq` |
| `ytm` | 到期收益率 | `--price`, `--face`, `--coupon-rate`, `--years`, `--freq` |
| `ytc` | 赎回收益率 | `--price`, `--face`, `--coupon-rate`, `--years-to-call`, `--call-price`, `--freq` |
| `current-yield` | 当前收益率 | `--price`, `--face`, `--coupon-rate` |
| `duration` | 麦考利久期和修正久期 | `--face`, `--coupon-rate`, `--ytm`, `--years`, `--freq` |
| `convexity` | 凸性 | `--face`, `--coupon-rate`, `--ytm`, `--years`, `--freq` |

## 输入格式说明

### 利率格式
- 使用小数格式：`0.05` 表示 5%
- 或百分比格式：`5`（将自动转换为 0.05）

### 列表格式
- 逗号分隔的值：`"0.10,0.15,0.12"`
- 不要有空格（或使用引号包含空格）

### 复利频率
- 年复利：`1`
- 半年复利：`2`
- 季度复利：`4`
- 月复利：`12`
- 周复利：`52`
- 日复利：`365`

## 实用技巧

### 1. 快速计算投资回报

计算 10 万元投资，年化收益率 8%，投资 5 年的终值：
```bash
cfa tvm fv --pv 100000 --rate 0.08 --n 5
```

### 2. 评估基金表现

假设某基金年收益率 15%，无风险利率 3%，标准差 18%：
```bash
cfa portfolio sharpe --return 0.15 --rf 0.03 --std 0.18
```

### 3. 计算退休金需求

每月需要 5000 元，预期寿命 30 年，折现率 4%：
```bash
cfa tvm annuity --pmt 5000 --rate 0.003333 --n 360 --type pv
```
注意：月利率 = 年利率 / 12，期数 = 年数 × 12

### 4. 比较不同复利频率

年利率 6%，不同复利频率的有效年利率：
```bash
cfa tvm ear --stated-rate 0.06 --freq 1   # 年复利
cfa tvm ear --stated-rate 0.06 --freq 2   # 半年复利
cfa tvm ear --stated-rate 0.06 --freq 12  # 月复利
```

### 5. 评估债券投资

计算面值 10 万元，票面利率 5%，市场价格 9.5 万元，5 年到期的债券收益率：
```bash
cfa bond ytm --price 95000 --face 100000 --coupon-rate 0.05 --years 5 --freq 2
```

### 6. 计算债券久期风险

评估债券对利率变化的敏感度：
```bash
cfa bond duration --face 100000 --coupon-rate 0.04 --ytm 0.045 --years 7 --freq 2
```
修正久期越大，债券价格对利率变化越敏感。

### 7. 比较溢价债券和折价债券

**溢价债券**（票面利率 > 市场利率）：
```bash
cfa bond price --face 1000 --coupon-rate 0.07 --ytm 0.05 --years 10 --freq 2
# 价格 > 1000
```

**折价债券**（票面利率 < 市场利率）：
```bash
cfa bond price --face 1000 --coupon-rate 0.04 --ytm 0.06 --years 10 --freq 2
# 价格 < 1000
```

## 开发

### 运行测试

```bash
pytest tests/ -v
```

### 运行测试并查看覆盖率

```bash
pytest tests/ -v --cov=src/cfa_calculator --cov-report=term-missing
```

### 项目结构

```
Calculator CLI/
├── src/cfa_calculator/
│   ├── main.py              # CLI 入口点
│   ├── commands/            # 命令模块
│   │   ├── tvm.py
│   │   └── portfolio.py
│   ├── formulas/            # 核心计算逻辑
│   │   ├── tvm_formulas.py
│   │   └── portfolio_formulas.py
│   └── utils/               # 工具函数
│       ├── formatters.py
│       └── validators.py
└── tests/                   # 测试套件
```

## 开发路线图

### ✅ 第一阶段（已完成）
- 货币时间价值计算
- 投资组合管理计算
- 固定收益计算（债券定价、YTM、YTC、久期、凸性）

### 第二阶段（即将推出）
- 统计学模块（均值、标准差、偏度、峰度、置信区间）
- 其他计算（NPV、IRR、货币加权收益率 vs 时间加权收益率）

### 第三阶段（未来）
- 股权估值（DDM、FCFE、市盈率）
- 衍生品（Black-Scholes、二叉树模型、看涨看跌平价关系）

### 第四阶段（高级功能）
- 保存/加载计算会话
- 导出结果为 CSV/JSON
- 公式参考查询
- 多货币支持

## 常见问题

### Q: 如何输入百分比？
A: 可以使用小数（0.05）或整数（5），工具会自动识别。

### Q: 计算结果不准确？
A: 请确保：
- 利率使用小数形式（5% = 0.05）
- 期数单位与利率单位一致（年利率对应年数）
- 复利频率设置正确

### Q: 如何查看公式？
A: 在任何命令后添加 `--explain` 标志。

## 贡献

欢迎贡献！请确保：
- 所有公式与 CFA 课程完全一致
- 新功能包含测试
- 代码遵循现有风格规范

## 许可证

MIT License

## 支持

如有问题或建议，请在项目仓库中提交 issue。

## 致谢

为全球 CFA 考生和金融专业人士打造。
