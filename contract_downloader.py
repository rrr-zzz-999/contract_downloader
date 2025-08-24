#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能合约源代码下载器
支持从多个区块链网络下载验证的智能合约源代码
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, Optional, List
import argparse

class ContractDownloader:
    """智能合约下载器类"""
    
    def __init__(self):
        # 支持的链和对应的API配置
        self.chain_configs = {
            "1": {  # Ethereum Mainnet
                "name": "Ethereum",
                "api_url": "https://api.etherscan.io/api",
                "api_key_env": "ETHERSCAN_API_KEY",
                "explorer_url": "https://etherscan.io"
            },
            "56": {  # BSC Mainnet
                "name": "BSC",
                "api_url": "https://api.bscscan.com/api",
                "api_key_env": "BSCSCAN_API_KEY", 
                "explorer_url": "https://bscscan.com"
            },
            "137": {  # Polygon Mainnet
                "name": "Polygon",
                "api_url": "https://api.polygonscan.com/api",
                "api_key_env": "POLYGONSCAN_API_KEY",
                "explorer_url": "https://polygonscan.com"
            },
            "250": {  # Fantom Mainnet
                "name": "Fantom",
                "api_url": "https://api.ftmscan.com/api",
                "api_key_env": "FTMSCAN_API_KEY",
                "explorer_url": "https://ftmscan.com"
            },
            "43114": {  # Avalanche Mainnet
                "name": "Avalanche",
                "api_url": "https://api.snowtrace.io/api",
                "api_key_env": "SNOWTRACE_API_KEY",
                "explorer_url": "https://snowtrace.io"
            },
            "42161": {  # Arbitrum One
                "name": "Arbitrum",
                "api_url": "https://api.arbiscan.io/api",
                "api_key_env": "ARBISCAN_API_KEY",
                "explorer_url": "https://arbiscan.io"
            },
            "10": {  # Optimism
                "name": "Optimism",
                "api_url": "https://api-optimistic.etherscan.io/api",
                "api_key_env": "OPTIMISM_API_KEY",
                "explorer_url": "https://optimistic.etherscan.io"
            }
        }
        
        # 创建输出目录
        self.output_dir = Path("contracts")
        self.output_dir.mkdir(exist_ok=True)
    
    def get_api_key(self, chain_id: str) -> Optional[str]:
        """获取对应链的API密钥"""
        if chain_id not in self.chain_configs:
            return None
        
        env_var = self.chain_configs[chain_id]["api_key_env"]
        api_key = os.getenv(env_var)
        
        if not api_key:
            print(f"警告: 未找到 {env_var} 环境变量，将使用无API密钥模式（可能受到速率限制）")
        
        return api_key
    
    def is_valid_address(self, address: str) -> bool:
        """验证以太坊地址格式"""
        if not address.startswith("0x"):
            return False
        if len(address) != 42:
            return False
        try:
            int(address[2:], 16)
            return True
        except ValueError:
            return False
    
    def get_contract_source(self, chain_id: str, contract_address: str, block_number: Optional[str] = None) -> Optional[Dict]:
        """从区块链浏览器API获取合约源代码"""
        if chain_id not in self.chain_configs:
            print(f"错误: 不支持的链ID {chain_id}")
            print(f"支持的链ID: {', '.join(self.chain_configs.keys())}")
            return None
        
        if not self.is_valid_address(contract_address):
            print(f"错误: 无效的合约地址格式 {contract_address}")
            return None
        
        config = self.chain_configs[chain_id]
        api_key = self.get_api_key(chain_id)
        
        # 构建API请求参数
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": contract_address
        }
        
        if api_key:
            params["apikey"] = api_key
        
        if block_number:
            params["tag"] = block_number
        
        try:
            print(f"正在从 {config['name']} 网络获取合约源代码...")
            print(f"合约地址: {contract_address}")
            if block_number:
                print(f"区块号: {block_number}")
            
            response = requests.get(config["api_url"], params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "1":
                print(f"API错误: {data.get('message', '未知错误')}")
                return None
            
            result = data.get("result", [])
            if not result or not result[0]:
                print("错误: 未找到合约源代码或合约未验证")
                return None
            
            contract_data = result[0]
            
            if not contract_data.get("SourceCode"):
                print("错误: 合约源代码为空或未验证")
                return None
            
            return contract_data
            
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None
    
    def save_contract_files(self, chain_id: str, contract_address: str, contract_data: Dict, block_number: Optional[str] = None) -> bool:
        """保存合约文件到本地"""
        try:
            chain_name = self.chain_configs[chain_id]["name"]
            contract_name = contract_data.get("ContractName", "Unknown")
            
            # 创建目录结构
            if block_number:
                dir_name = f"{chain_name}_{contract_address}_{block_number}"
            else:
                dir_name = f"{chain_name}_{contract_address}"
            
            contract_dir = self.output_dir / dir_name
            contract_dir.mkdir(exist_ok=True)
            
            source_code = contract_data.get("SourceCode", "")
            
            # 处理多文件合约（Proxy合约等）
            if source_code.startswith("{"):
                try:
                    # 尝试解析JSON格式的多文件源代码
                    if source_code.startswith("{{"):
                        source_code = source_code[1:-1]  # 移除外层大括号
                    
                    source_json = json.loads(source_code)
                    
                    if "sources" in source_json:
                        # 标准格式
                        sources = source_json["sources"]
                        settings = source_json.get("settings", {})
                        
                        # 保存设置文件
                        with open(contract_dir / "compiler_settings.json", "w", encoding="utf-8") as f:
                            json.dump(settings, f, indent=2, ensure_ascii=False)
                        
                        # 保存每个源文件
                        for file_path, file_data in sources.items():
                            content = file_data.get("content", "")
                            
                            # 创建文件路径
                            file_full_path = contract_dir / file_path.lstrip("/")
                            file_full_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            with open(file_full_path, "w", encoding="utf-8") as f:
                                f.write(content)
                            
                            print(f"已保存: {file_full_path}")
                    else:
                        # 其他格式，尝试直接处理
                        main_file = contract_dir / f"{contract_name}.sol"
                        with open(main_file, "w", encoding="utf-8") as f:
                            f.write(source_code)
                        print(f"已保存: {main_file}")
                        
                except json.JSONDecodeError:
                    # 如果不是JSON格式，当作普通源代码处理
                    main_file = contract_dir / f"{contract_name}.sol"
                    with open(main_file, "w", encoding="utf-8") as f:
                        f.write(source_code)
                    print(f"已保存: {main_file}")
            else:
                # 单文件合约
                main_file = contract_dir / f"{contract_name}.sol"
                with open(main_file, "w", encoding="utf-8") as f:
                    f.write(source_code)
                print(f"已保存: {main_file}")
            
            # 保存合约元数据
            metadata = {
                "contract_name": contract_name,
                "contract_address": contract_address,
                "chain_id": chain_id,
                "chain_name": chain_name,
                "compiler_version": contract_data.get("CompilerVersion", ""),
                "optimization_used": contract_data.get("OptimizationUsed", ""),
                "runs": contract_data.get("Runs", ""),
                "constructor_arguments": contract_data.get("ConstructorArguments", ""),
                "library": contract_data.get("Library", ""),
                "license_type": contract_data.get("LicenseType", ""),
                "proxy": contract_data.get("Proxy", ""),
                "implementation": contract_data.get("Implementation", ""),
                "swarm_source": contract_data.get("SwarmSource", "")
            }
            
            if block_number:
                metadata["block_number"] = block_number
            
            with open(contract_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"已保存元数据: {contract_dir / 'metadata.json'}")
            print(f"合约文件已成功下载到: {contract_dir}")
            
            return True
            
        except Exception as e:
            print(f"保存文件时出错: {e}")
            return False
    
    def download_contract(self, chain_id: str, contract_address: str, block_number: Optional[str] = None) -> bool:
        """下载合约的主要方法"""
        print("=" * 60)
        print("智能合约源代码下载器")
        print("=" * 60)
        
        # 获取合约源代码
        contract_data = self.get_contract_source(chain_id, contract_address, block_number)
        if not contract_data:
            return False
        
        # 显示合约信息
        print(f"\n合约信息:")
        print(f"  名称: {contract_data.get('ContractName', 'Unknown')}")
        print(f"  编译器版本: {contract_data.get('CompilerVersion', 'Unknown')}")
        print(f"  优化: {contract_data.get('OptimizationUsed', 'Unknown')}")
        print(f"  许可证: {contract_data.get('LicenseType', 'Unknown')}")
        
        # 保存文件
        success = self.save_contract_files(chain_id, contract_address, contract_data, block_number)
        
        if success:
            print(f"\n✅ 合约下载完成!")
            return True
        else:
            print(f"\n❌ 合约下载失败!")
            return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智能合约源代码下载器")
    parser.add_argument("contract_address", help="合约地址")
    parser.add_argument("chain_id", help="链ID (1=Ethereum, 56=BSC, 137=Polygon, 等)")
    parser.add_argument("--block", "-b", help="区块号 (可选)", default=None)
    parser.add_argument("--list-chains", "-l", action="store_true", help="显示支持的链")
    
    args = parser.parse_args()
    
    downloader = ContractDownloader()
    
    if args.list_chains:
        print("支持的区块链网络:")
        for chain_id, config in downloader.chain_configs.items():
            print(f"  {chain_id}: {config['name']} ({config['explorer_url']})")
        return
    
    # 下载合约
    success = downloader.download_contract(args.chain_id, args.contract_address, args.block)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
