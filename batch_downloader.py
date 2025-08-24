#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量合约下载器
支持从JSON数组、CSV文件或直接代码中的数组批量下载智能合约源代码
"""

import json
import csv
from contract_downloader import ContractDownloader

def download_from_array(contracts_array):
    """从Python数组直接下载合约"""
    downloader = ContractDownloader()
    return downloader.download_contracts_batch(contracts_array)

def download_from_json_file(json_file_path):
    """从JSON文件下载合约"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            contracts = json.load(f)
        
        if not isinstance(contracts, list):
            print("错误: JSON文件应包含合约信息数组")
            return None
        
        downloader = ContractDownloader()
        return downloader.download_contracts_batch(contracts)
        
    except FileNotFoundError:
        print(f"错误: 文件 '{json_file_path}' 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"错误: JSON文件格式错误: {e}")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def download_from_csv_file(csv_file_path):
    """从CSV文件下载合约"""
    try:
        contracts = []
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contract = {}
                
                # 处理常见的列名映射
                for key, value in row.items():
                    key_lower = key.lower().strip()
                    
                    if key_lower in ['name', 'contract_name', '名称']:
                        contract['name'] = value.strip()
                    elif key_lower in ['chain', 'network', '链', '网络']:
                        contract['chain'] = value.strip()
                    elif key_lower in ['address', 'contract_address', '地址', '合约地址']:
                        contract['address'] = value.strip()
                    elif key_lower in ['height', 'block', 'block_number', '区块', '区块号']:
                        if value.strip():
                            contract['height'] = value.strip()
                    elif key_lower in ['date', '日期']:
                        contract['date'] = value.strip()
                
                if contract.get('address'):  # 只有地址不为空才添加
                    contracts.append(contract)
        
        if not contracts:
            print("错误: CSV文件中没有找到有效的合约信息")
            return None
        
        downloader = ContractDownloader()
        return downloader.download_contracts_batch(contracts)
        
    except FileNotFoundError:
        print(f"错误: 文件 '{csv_file_path}' 不存在")
        return None
    except Exception as e:
        print(f"错误: 读取CSV文件时出错: {e}")
        return None

def main():
    """示例用法"""
    
    # 示例1: 从代码中的数组下载
    print("示例1: 从代码数组下载")
    contracts_array = [
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
    
    results = download_from_array(contracts_array)
    if results:
        print("从数组下载完成!")
    
    print("\n" + "="*80 + "\n")
    
    # 示例2: 从JSON文件下载
    print("示例2: 从JSON文件下载")
    results = download_from_json_file("contracts_example.json")
    if results:
        print("从JSON文件下载完成!")
    
    print("\n" + "="*80 + "\n")
    
    # 示例3: 从CSV文件下载（如果存在）
    print("示例3: 从CSV文件下载")
    results = download_from_csv_file("contracts_example.csv")
    if results:
        print("从CSV文件下载完成!")

if __name__ == "__main__":
    main()
