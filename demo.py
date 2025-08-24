#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的使用示例
演示如何使用不同方式批量下载合约
使用 .env 文件管理配置
"""

import os

# 尝试加载 dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()  # 加载 .env 文件
    print("✅ 已加载 .env 配置文件")
except ImportError:
    print("⚠️  未安装 python-dotenv，运行: pip install python-dotenv")

from contract_downloader import ContractDownloader

def demo_array_download():
    """演示从数组下载"""
    print("=" * 60)
    print("演示1: 从Python数组批量下载")
    print("=" * 60)
    
    # 基于你提供的表格数据的合约数组
    contracts = [
        {
            "name": "uranium",
            "date": "2021-4-27",
            "chain": "bsc",
            "height": "6920000",
            "address": "0xbb4Cd89Cd6B01bD1cBaEBF2De08d9173bc095c"
        },
        {
            "name": "valuedefi",
            "date": "2021-5-8", 
            "chain": "bsc",
            "height": "7223029",
            "address": "0x7Af938f0EFDD98Dc5131109F6A7E51106D26E16c"
        },
        {
            "name": "pancakehunny",
            "date": "2021-6-3",
            "chain": "bsc", 
            "height": "7962338",
            "address": "0x565b72163f17849832A692A3c5928cc502f46D69"
        }
    ]
    
    print(f"准备下载 {len(contracts)} 个合约...")
    downloader = ContractDownloader()
    results = downloader.download_contracts_batch(contracts)
    
    if results:
        success_count = sum(1 for success in results.values() if success)
        print(f"\n✅ 数组下载完成! 成功: {success_count}/{len(contracts)}")
    else:
        print("\n❌ 数组下载失败!")

def demo_json_download():
    """演示从JSON文件下载"""
    print("\n" + "=" * 60)
    print("演示2: 从JSON文件批量下载")
    print("=" * 60)
    
    # 使用命令行方式演示
    import subprocess
    try:
        result = subprocess.run(
            ["python", "contract_downloader.py", "--batch", "contracts_example.json"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            print("✅ JSON文件下载完成!")
            results = True
        else:
            print(f"❌ JSON文件下载失败: {result.stderr}")
            results = False
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        results = False
    
def demo_csv_download():
    """演示从CSV文件下载"""
    print("\n" + "=" * 60)
    print("演示3: 从CSV文件批量下载")
    print("=" * 60)
    
    # 使用命令行方式演示
    import subprocess
    try:
        result = subprocess.run(
            ["python", "contract_downloader.py", "--batch", "contracts_example.csv"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            print("✅ CSV文件下载完成!")
            results = True
        else:
            print(f"❌ CSV文件下载失败: {result.stderr}")
            results = False
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        results = False

def main():
    """主演示函数"""
    print("智能合约批量下载器 - 完整演示")
    print("支持的输入格式:")
    print("  1. Python数组/列表")
    print("  2. JSON文件")
    print("  3. CSV文件")
    print()
    
    # 选择运行哪个演示
    print("选择演示项目:")
    print("  1. 从Python数组下载")
    print("  2. 从JSON文件下载") 
    print("  3. 从CSV文件下载")
    print("  4. 运行所有演示")
    
    try:
        choice = input("\n请输入选择 (1-4, 默认4): ").strip()
        if not choice:
            choice = "4"
        
        if choice == "1":
            demo_array_download()
        elif choice == "2":
            demo_json_download()
        elif choice == "3":
            demo_csv_download()
        elif choice == "4":
            demo_array_download()
            demo_json_download() 
            demo_csv_download()
        else:
            print("无效选择，运行所有演示...")
            demo_array_download()
            demo_json_download()
            demo_csv_download()
            
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
    except Exception as e:
        print(f"\n演示过程中出错: {e}")
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("下载的合约文件保存在 ./contracts/ 目录下")
    print("=" * 60)

if __name__ == "__main__":
    main()
