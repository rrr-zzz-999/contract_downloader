# 智能合约源代码下载器

这个项目可以根据合约地址、链编号和区块号批量下载对应的 Solidity 源代码到本地。支持使用 `.env` 文件管理 API 密钥和配置。

## 🚀 功能特性

- ✅ 支持多个主流区块链网络 (Ethereum、BSC、Polygon 等)
- ✅ 批量下载功能 (JSON、CSV、数组)
- ✅ 自动处理单文件和多文件合约
- ✅ 保存完整合约元数据信息
- ✅ 支持指定区块号获取历史版本
- ✅ 使用 `.env` 文件管理 API 密钥
- ✅ 智能错误处理和重试机制
- ✅ 自动创建目录结构

## 📋 支持的区块链

| 链ID | 网络名称 | 简称 | 浏览器 |
|------|----------|------|--------|
| 1    | Ethereum | eth | etherscan.io |
| 56   | BSC      | bsc | bscscan.com |
| 137  | Polygon  | polygon | polygonscan.com |
| 250  | Fantom   | fantom | ftmscan.com |
| 43114| Avalanche| avalanche | snowtrace.io |
| 42161| Arbitrum | arbitrum | arbiscan.io |
| 10   | Optimism | optimism | optimistic.etherscan.io |

## 🔧 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制示例配置文件：
```bash
cp env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```bash
# 区块链浏览器 API 密钥配置
ETHERSCAN_API_KEY=your_etherscan_api_key_here
BSCSCAN_API_KEY=your_bscscan_api_key_here
POLYGONSCAN_API_KEY=your_polygonscan_api_key_here
FTMSCAN_API_KEY=your_ftmscan_api_key_here
SNOWTRACE_API_KEY=your_snowtrace_api_key_here
ARBISCAN_API_KEY=your_arbiscan_api_key_here
OPTIMISM_API_KEY=your_optimism_api_key_here

# 通用配置
DOWNLOAD_DELAY=1          # 下载延迟 (秒)
OUTPUT_DIR=contracts      # 输出目录
VERBOSE=true             # 启用详细日志
```

### 3. 获取 API 密钥

访问对应的区块链浏览器网站获取免费 API 密钥：

- **Ethereum**: https://etherscan.io/apis
- **BSC**: https://bscscan.com/apis  
- **Polygon**: https://polygonscan.com/apis
- **Fantom**: https://ftmscan.com/apis
- **Avalanche**: https://snowtrace.io/apis
- **Arbitrum**: https://arbiscan.io/apis
- **Optimism**: https://optimistic.etherscan.io/apis

> 💡 **提示**: 虽然可以不配置 API 密钥使用，但会受到严格的速率限制。强烈建议配置 API 密钥以获得更好的下载体验。

## 📖 使用方法

### 单个合约下载

```bash
# 基本用法
python contract_downloader.py <合约地址> <链ID>

# 指定区块号
python contract_downloader.py <合约地址> <链ID> --block <区块号>

# 查看支持的链
python contract_downloader.py --list-chains
```

### 批量下载

#### 方法1: 从 JSON 文件批量下载
```bash
python contract_downloader.py --batch contracts_full.json
```

#### 方法2: 使用演示脚本
```bash
python demo.py
```

#### 方法3: 在代码中使用
```python
from contract_downloader import ContractDownloader

contracts = [
    {
        "name": "uranium",
        "chain": "bsc",
        "height": "6920000", 
        "address": "0x9B9baD4c6513E0fF3fB77c739359D59601c7cAfF"
    }
]

downloader = ContractDownloader()
results = downloader.download_contracts_batch(contracts)
```

## 📊 数据格式

### JSON 格式示例
```json
[
  {
    "name": "uranium",
    "chain": "bsc",
    "height": "6920000",
    "address": "0x9B9baD4c6513E0fF3fB77c739359D59601c7cAfF"
  },
  {
    "name": "valuedefi",
    "chain": "bsc", 
    "height": "7223029",
    "address": "0x7Af938f0EFDD98Dc5131109F6A7E51106D26E16c"
  }
]
```

### CSV 格式示例
```csv
name,chain,block,contract
uranium,56,6920000,0x9B9baD4c6513E0fF3fB77c739359D59601c7cAfF
valuedefi,56,7223029,0x7Af938f0EFDD98Dc5131109F6A7E51106D26E16c
```

### 支持的字段

| 字段名 | 说明 | 必填 | 示例 |
|--------|------|------|------|
| name | 合约名称 | 否 | "uranium" |
| chain | 链标识 | 是 | "bsc", "eth", "56", "1" |
| address/contract | 合约地址 | 是 | "0x..." |
| height/block | 区块号 | 否 | "6920000" |
| date | 日期 | 否 | "2021-4-27" |

## 🎯 使用示例

### 下载 Ethereum 上的 USDT 合约
```bash
python contract_downloader.py 0xdAC17F958D2ee523a2206206994597C13D831ec7 1
```

### 下载 BSC 上的 PancakeSwap 合约
```bash
python contract_downloader.py 0x10ED43C718714eb63d5aA57B78B54704E256024E 56
```

### 下载指定区块号的合约
```bash
python contract_downloader.py 0xdAC17F958D2ee523a2206206994597C13D831ec7 1 --block 18500000
```

### 批量下载示例
```bash
# 使用提供的示例数据
python contract_downloader.py --batch contracts_full.csv

# 或使用交互式脚本
python demo.py
```

## 📁 输出结构

下载的文件将保存在配置的输出目录下（默认 `contracts/`），结构如下：

```
contracts/
└── BSC_0x9B9baD4c6513E0fF3fB77c739359D59601c7cAfF_6920000/
    ├── Uranium.sol              # 主合约文件
    ├── metadata.json            # 合约元数据
    └── compiler_settings.json   # 编译器设置（多文件合约）
```

对于多文件合约，会保持原有的目录结构：

```
contracts/
└── Ethereum_0x1234.../
    ├── contracts/
    │   ├── Token.sol
    │   └── interfaces/
    │       └── IERC20.sol
    ├── metadata.json
    └── compiler_settings.json
```

## 🔧 高级配置

### 环境变量详解

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `*_API_KEY` | 各链的 API 密钥 | 无 | "ABCD1234..." |
| `DOWNLOAD_DELAY` | 下载延迟 (秒) | 1 | "2" |
| `OUTPUT_DIR` | 输出目录 | "contracts" | "my_contracts" |
| `VERBOSE` | 详细日志 | "true" | "false" |

### 自定义配置示例

```bash
# .env 文件
OUTPUT_DIR=my_contracts
DOWNLOAD_DELAY=2
VERBOSE=false
ETHERSCAN_API_KEY=your_key_here
```

## 🚨 注意事项

1. **API 限制**: 无 API 密钥时受到严格速率限制
2. **合约验证**: 只能下载已验证的合约源代码
3. **网络稳定**: 确保网络连接稳定，避免下载中断
4. **文件权限**: 确保有写入输出目录的权限
5. **代理合约**: 某些代理合约可能需要特殊处理

## 🐛 常见问题

### Q: 下载失败怎么办？
A: 检查网络连接、API 密钥配置和合约地址是否正确

### Q: 支持测试网吗？
A: 当前主要支持主网，可以通过修改配置文件添加测试网支持

### Q: 如何提高下载速度？
A: 配置 API 密钥并适当调整 `DOWNLOAD_DELAY` 参数

### Q: CSV 文件格式有要求吗？
A: 支持多种列名格式，详见"支持的字段"部分

## 📝 更新日志

- **v2.0**: 添加 .env 配置支持，重构项目结构
- **v1.0**: 基础批量下载功能，支持多链和多格式

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License