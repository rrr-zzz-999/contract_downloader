#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境配置助手
帮助用户快速配置 .env 文件
"""

import os
from pathlib import Path

def create_env_file():
    """创建 .env 文件的交互式助手"""
    print("=" * 60)
    print("智能合约下载器 - 环境配置助手")
    print("=" * 60)
    print()
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  发现已存在的 .env 文件")
        overwrite = input("是否覆盖现有配置? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("配置已取消")
            return
    
    print("请输入区块链浏览器的 API 密钥 (留空跳过):")
    print("💡 提示: API 密钥是可选的，但强烈建议配置以避免速率限制")
    print()
    
    # API 密钥配置
    api_keys = {}
    
    chains = [
        ("ETHERSCAN_API_KEY", "Ethereum", "https://etherscan.io/apis"),
        ("BSCSCAN_API_KEY", "BSC", "https://bscscan.com/apis"),
        ("POLYGONSCAN_API_KEY", "Polygon", "https://polygonscan.com/apis"),
        ("FTMSCAN_API_KEY", "Fantom", "https://ftmscan.com/apis"),
        ("SNOWTRACE_API_KEY", "Avalanche", "https://snowtrace.io/apis"),
        ("ARBISCAN_API_KEY", "Arbitrum", "https://arbiscan.io/apis"),
        ("OPTIMISM_API_KEY", "Optimism", "https://optimistic.etherscan.io/apis")
    ]
    
    for env_var, name, url in chains:
        print(f"📋 {name} API Key ({url}):")
        key = input(f"   {env_var}: ").strip()
        if key:
            api_keys[env_var] = key
        print()
    
    # 通用配置
    print("📝 通用配置:")
    download_delay = input("   下载延迟 (秒, 默认: 1): ").strip() or "1"
    output_dir = input("   输出目录 (默认: contracts): ").strip() or "contracts"
    verbose = input("   启用详细日志? (Y/n): ").strip().lower()
    verbose = "false" if verbose == "n" else "true"
    
    # 生成 .env 文件内容
    env_content = [
        "# 智能合约下载器环境配置",
        "# 由配置助手自动生成",
        "",
        "# 区块链浏览器 API 密钥配置",
    ]
    
    for env_var, name, url in chains:
        env_content.append(f"# {name} - {url}")
        if env_var in api_keys:
            env_content.append(f"{env_var}={api_keys[env_var]}")
        else:
            env_content.append(f"# {env_var}=your_api_key_here")
        env_content.append("")
    
    env_content.extend([
        "# 通用配置",
        f"DOWNLOAD_DELAY={download_delay}",
        f"OUTPUT_DIR={output_dir}",
        f"VERBOSE={verbose}",
        ""
    ])
    
    # 写入文件
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write("\n".join(env_content))
        
        print("✅ .env 文件已创建成功!")
        print(f"📁 配置文件位置: {Path('.env').absolute()}")
        print()
        
        # 显示配置摘要
        print("📋 配置摘要:")
        configured_keys = len(api_keys)
        total_keys = len(chains)
        print(f"   API 密钥: {configured_keys}/{total_keys} 已配置")
        print(f"   下载延迟: {download_delay} 秒")
        print(f"   输出目录: {output_dir}")
        print(f"   详细日志: {verbose}")
        print()
        
        if configured_keys == 0:
            print("⚠️  警告: 未配置任何 API 密钥，可能会受到速率限制")
            print("   建议至少配置常用链的 API 密钥")
        elif configured_keys < total_keys:
            print("💡 提示: 可以稍后添加更多 API 密钥以支持更多区块链")
        
        print()
        print("🚀 现在可以开始使用智能合约下载器了!")
        print("   python contract_downloader.py --list-chains")
        print("   python contract_downloader.py --batch contracts_full.csv")
        
    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")

def check_env_status():
    """检查当前环境配置状态"""
    print("=" * 60)
    print("环境配置状态检查")
    print("=" * 60)
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ 未找到 .env 文件")
        print("   运行 'python setup.py' 创建配置文件")
        return
    
    print("✅ .env 文件存在")
    print()
    
    # 尝试加载 dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ python-dotenv 已安装")
    except ImportError:
        print("❌ python-dotenv 未安装")
        print("   运行: pip install python-dotenv")
        return
    
    print()
    print("API 密钥配置状态:")
    
    api_keys = [
        ("ETHERSCAN_API_KEY", "Ethereum"),
        ("BSCSCAN_API_KEY", "BSC"),
        ("POLYGONSCAN_API_KEY", "Polygon"),
        ("FTMSCAN_API_KEY", "Fantom"),
        ("SNOWTRACE_API_KEY", "Avalanche"),
        ("ARBISCAN_API_KEY", "Arbitrum"),
        ("OPTIMISM_API_KEY", "Optimism")
    ]
    
    configured_count = 0
    for env_var, name in api_keys:
        value = os.getenv(env_var)
        if value:
            print(f"   ✅ {name}: 已配置")
            configured_count += 1
        else:
            print(f"   ❌ {name}: 未配置")
    
    print()
    print("通用配置:")
    print(f"   下载延迟: {os.getenv('DOWNLOAD_DELAY', '1')} 秒")
    print(f"   输出目录: {os.getenv('OUTPUT_DIR', 'contracts')}")
    print(f"   详细日志: {os.getenv('VERBOSE', 'true')}")
    
    print()
    print(f"📊 总计: {configured_count}/{len(api_keys)} API 密钥已配置")
    
    if configured_count == 0:
        print("⚠️  建议配置至少一个 API 密钥以获得更好的体验")

def main():
    """主函数"""
    print("智能合约下载器 - 配置助手")
    print()
    print("选择操作:")
    print("  1. 创建/更新 .env 配置文件")
    print("  2. 检查当前配置状态")
    print("  3. 退出")
    
    try:
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            create_env_file()
        elif choice == "2":
            check_env_status()
        elif choice == "3":
            print("再见!")
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n发生错误: {e}")

if __name__ == "__main__":
    main()
