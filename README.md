# 智能合约源码下载器

这个脚本可以帮助你从各种区块链网络下载智能合约的源码到本地。

## 功能特性

- 支持多个主流区块链网络（以太坊、BSC、Polygon、Arbitrum、Optimism等）
- 支持测试网络（Goerli、Sepolia）
- 自动处理单文件和多文件合约
- 保存完整的合约信息
- 支持API密钥配置以避免速率限制

## 支持的区块链

| 链ID | 网络名称 | API提供商 |
|------|----------|-----------|
| 1 | Ethereum Mainnet | Etherscan |
| 5 | Goerli Testnet | Etherscan |
| 11155111 | Sepolia Testnet | Etherscan |
| 56 | BSC Mainnet | BSCScan |
| 137 | Polygon Mainnet | Polygonscan |
| 42161 | Arbitrum One | Arbiscan |
| 10 | Optimism | Optimism Etherscan |

## 安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置API密钥（可选但推荐）：
```bash
cp config.json.example config.json
# 编辑config.json文件，填入你的API密钥
```

或者设置环境变量：
```bash
export ETHERSCAN_API_KEY="你的API密钥"
export BSCSCAN_API_KEY="你的API密钥"
export POLYGONSCAN_API_KEY="你的API密钥"
# ... 其他API密钥
```

## 使用方法

### 基本用法

```bash
python contract_downloader.py <合约地址> <链ID>
```

### 示例

1. 下载以太坊主网上的合约：
```bash
python contract_downloader.py 0xA0b86a33E6441E95Bb4Cd2654b6b5a1b2e5c2b1f 1
```

2. 下载BSC主网上的合约：
```bash
python contract_downloader.py 0x123...abc 56
```

3. 指定区块号（可选）：
```bash
python contract_downloader.py 0x123...abc 1 --block 18500000
```

4. 指定输出目录：
```bash
python contract_downloader.py 0x123...abc 1 --output ./my_contracts
```

### 命令行参数

- `contract_address`: 合约地址（必需）
- `chain_id`: 链ID（必需）
- `--block`: 指定区块号（可选）
- `--output, -o`: 输出目录（默认：contracts）
- `--config, -c`: 配置文件路径（默认：config.json）

## 输出结构

下载的文件会按以下结构组织：

```
contracts/
├── Ethereum/
│   └── 0x123...abc/
│       ├── ContractName.sol
│       ├── imports/
│       │   └── LibraryName.sol
│       └── contract_info.json
└── BSC/
    └── 0x456...def/
        └── ...
```

## API密钥获取

1. **Etherscan**: https://etherscan.io/apis
2. **BSCScan**: https://bscscan.com/apis
3. **Polygonscan**: https://polygonscan.com/apis
4. **Arbiscan**: https://arbiscan.io/apis
5. **Optimism Etherscan**: https://optimistic.etherscan.io/apis

## 注意事项

- 没有API密钥时会使用免费API，有速率限制
- 某些合约可能没有公开源码
- 确保合约地址格式正确（0x开头，42位十六进制）
- 网络请求可能需要一些时间，请耐心等待

## 错误处理

脚本包含详细的错误处理和用户友好的提示信息，会告诉你具体的问题所在。

## 许可证

MIT License
