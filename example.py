#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例脚本
演示如何使用 ContractDownloader 类
"""

from contract_downloader import ContractDownloader

def main():
    """示例用法"""
    downloader = ContractDownloader()
    
    # 示例1: 下载 Ethereum 上的 USDT 合约
    print("示例1: 下载 USDT 合约")
    success = downloader.download_contract(
        chain_id="1",
        contract_address="0xdAC17F958D2ee523a2206206994597C13D831ec7"
    )
    
    if success:
        print("USDT 合约下载成功!")
    else:
        print("USDT 合约下载失败!")
    
    print("\n" + "="*60 + "\n")
    
    # 示例2: 下载 BSC 上的 PancakeSwap 路由合约
    print("示例2: 下载 PancakeSwap 路由合约")
    success = downloader.download_contract(
        chain_id="56",
        contract_address="0x10ED43C718714eb63d5aA57B78B54704E256024E"
    )
    
    if success:
        print("PancakeSwap 合约下载成功!")
    else:
        print("PancakeSwap 合约下载失败!")
    
    print("\n" + "="*60 + "\n")
    
    # 示例3: 下载指定区块的合约
    print("示例3: 下载指定区块的合约")
    success = downloader.download_contract(
        chain_id="1",
        contract_address="0xA0b86a33E6417c94e5a4cd5C93a8Bc8e6f6b9B84",  # Compound cETH
        block_number="18000000"
    )
    
    if success:
        print("指定区块合约下载成功!")
    else:
        print("指定区块合约下载失败!")

if __name__ == "__main__":
    main()
