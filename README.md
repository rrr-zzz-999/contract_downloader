# 智能合约源代码下载器

这个脚本可以根据合约地址、链编号和区块号下载对应的 Solidity 源代码到本地。

## 功能特性

- 支持多个主流区块链网络
- 自动处理单文件和多文件合约
- 保存合约元数据信息
- 支持指定区块号获取历史版本
- 自动创建目录结构

## 支持的区块链

| 链ID | 网络名称 | 浏览器 |
|------|----------|--------|
| 1    | Ethereum | etherscan.io |
| 56   | BSC      | bscscan.com |
| 137  | Polygon  | polygonscan.com |
| 250  | Fantom   | ftmscan.com |
| 43114| Avalanche| snowtrace.io |
| 42161| Arbitrum | arbiscan.io |
| 10   | Optimism | optimistic.etherscan.io |

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境变量配置（可选）

为了避免API速率限制，建议设置相应的API密钥：

```bash
export ETHERSCAN_API_KEY="your_etherscan_api_key"
export BSCSCAN_API_KEY="your_bscscan_api_key"
export POLYGONSCAN_API_KEY="your_polygonscan_api_key"
export FTMSCAN_API_KEY="your_ftmscan_api_key"
export SNOWTRACE_API_KEY="your_snowtrace_api_key"
export ARBISCAN_API_KEY="your_arbiscan_api_key"
export OPTIMISM_API_KEY="your_optimism_api_key"
```

## 使用方法

### 基本用法

```bash
python contract_downloader.py <合约地址> <链ID>
```

### 指定区块号

```bash
python contract_downloader.py <合约地址> <链ID> --block <区块号>
```

### 批量下载（从JSON文件）

```bash
python contract_downloader.py --batch contracts.json
```

### 查看支持的链

```bash
python contract_downloader.py --list-chains
```

### 批量下载脚本

使用专门的批量下载脚本：

```bash
python batch_downloader.py
```

## 使用示例

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

#### 从JSON文件批量下载
```bash
python contract_downloader.py --batch contracts_example.json
```

#### 使用专门的批量下载脚本
```bash
python batch_downloader.py
```

#### JSON文件格式示例
```json
[
  {
    "name": "uranium",
    "chain": "bsc",
    "height": "6920000",
    "address": "0xbb4Cd89Cd6B01bD1cBaEBF2De08d9173bc095c"
  },
  {
    "name": "valuedefi",
    "chain": "bsc", 
    "height": "7223029",
    "address": "0x7Af938f0EFDD98Dc5131109F6A7E51106D26E16c"
  }
]
```

#### CSV文件格式示例
```csv
Name,Date,Chain,Height,Address
uranium,2021-4-27,bsc,6920000,0xbb4Cd89Cd6B01bD1cBaEBF2De08d9173bc095c
valuedefi,2021-5-8,bsc,7223029,0x7Af938f0EFDD98Dc5131109F6A7E51106D26E16c
```

#### 在代码中使用批量下载
```python
from batch_downloader import download_from_array

contracts = [
    {
        "name": "uranium",
        "chain": "bsc",
        "height": "6920000", 
        "address": "0xbb4Cd89Cd6B01bD1cBaEBF2De08d9173bc095c"
    }
]

results = download_from_array(contracts)
```

## 输出结构

下载的文件将保存在 `contracts/` 目录下，结构如下：

```
contracts/
└── Ethereum_0xdAC17F958D2ee523a2206206994597C13D831ec7_18500000/
    ├── TetherToken.sol          # 主合约文件
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

## 注意事项

1. 只能下载已验证的合约源代码
2. 无API密钥时可能受到速率限制
3. 某些代理合约可能需要特殊处理
4. 网络连接问题可能导致下载失败

## 错误处理

- 无效的合约地址格式
- 不支持的链ID
- 未验证的合约
- 网络连接错误
- API限制错误
