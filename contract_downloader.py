#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能合约源代码下载器
支持从多个区块链网络下载验证的智能合约源代码
使用 .env 文件管理 API 密钥
"""

import os
import sys
import json
import csv
import time
import requests
from pathlib import Path
from typing import Dict, Optional, List
import argparse

# 尝试加载 dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()  # 加载 .env 文件
except ImportError:
    print("提示: 安装 python-dotenv 以使用 .env 文件管理 API 密钥")
    print("运行: pip install python-dotenv")

class ContractDownloader:
    """智能合约下载器类"""
    
    def __init__(self):
        # 支持 Etherscan V2 统一 API
        self.use_v2_api = os.getenv("USE_ETHERSCAN_V2", "true").lower() == "true"
        
        if self.use_v2_api:
            # Etherscan V2 - 统一配置，支持 50+ 条链
            self.chain_configs = {
                "1": {"name": "Ethereum", "explorer_url": "https://etherscan.io"},
                "56": {"name": "BSC", "explorer_url": "https://bscscan.com"},
                "137": {"name": "Polygon", "explorer_url": "https://polygonscan.com"},
                "250": {"name": "Fantom", "explorer_url": "https://ftmscan.com"},
                "43114": {"name": "Avalanche", "explorer_url": "https://snowtrace.io"},
                "42161": {"name": "Arbitrum", "explorer_url": "https://arbiscan.io"},
                "10": {"name": "Optimism", "explorer_url": "https://optimistic.etherscan.io"},
                "8453": {"name": "Base", "explorer_url": "https://basescan.org"},
                "534352": {"name": "Scroll", "explorer_url": "https://scrollscan.com"},
                "81457": {"name": "Blast", "explorer_url": "https://blastscan.io"},
                "5000": {"name": "Mantle", "explorer_url": "https://mantlescan.xyz"},
                "59144": {"name": "Linea", "explorer_url": "https://lineascan.build"}
            }
            # V2 统一端点和 API 密钥
            self.api_url = "https://api.etherscan.io/v2/api"
            self.api_key_env = "ETHERSCAN_API_KEY"
        else:
            # V1 API - 向后兼容
            self.chain_configs = {
                "1": {
                    "name": "Ethereum",
                    "api_url": "https://api.etherscan.io/api",
                    "api_key_env": "ETHERSCAN_API_KEY",
                    "explorer_url": "https://etherscan.io"
                },
                "56": {
                    "name": "BSC",
                    "api_url": "https://api.bscscan.com/api",
                    "api_key_env": "BSCSCAN_API_KEY", 
                    "explorer_url": "https://bscscan.com"
                },
                "137": {
                    "name": "Polygon",
                    "api_url": "https://api.polygonscan.com/api",
                    "api_key_env": "POLYGONSCAN_API_KEY",
                    "explorer_url": "https://polygonscan.com"
                },
                "250": {
                    "name": "Fantom",
                    "api_url": "https://api.ftmscan.com/api",
                    "api_key_env": "FTMSCAN_API_KEY",
                    "explorer_url": "https://ftmscan.com"
                },
                "43114": {
                    "name": "Avalanche",
                    "api_url": "https://api.snowtrace.io/api",
                    "api_key_env": "SNOWTRACE_API_KEY",
                    "explorer_url": "https://snowtrace.io"
                },
                "42161": {
                    "name": "Arbitrum",
                    "api_url": "https://api.arbiscan.io/api",
                    "api_key_env": "ARBISCAN_API_KEY",
                    "explorer_url": "https://arbiscan.io"
                },
                "10": {
                    "name": "Optimism",
                    "api_url": "https://api-optimistic.etherscan.io/api",
                    "api_key_env": "OPTIMISM_API_KEY",
                    "explorer_url": "https://optimistic.etherscan.io"
                }
            }
        
        # 从环境变量获取配置
        self.download_delay = float(os.getenv("DOWNLOAD_DELAY", "1"))
        self.verbose = os.getenv("VERBOSE", "true").lower() == "true"
        
        # 创建输出目录
        output_dir_name = os.getenv("OUTPUT_DIR", "contracts")
        self.output_dir = Path(output_dir_name)
        self.output_dir.mkdir(exist_ok=True)
    
    def get_api_key(self, chain_id: str) -> Optional[str]:
        """获取对应链的API密钥"""
        if chain_id not in self.chain_configs:
            return None
        
        if self.use_v2_api:
            # V2 API 使用统一的 API 密钥
            api_key = os.getenv(self.api_key_env)
            if not api_key and self.verbose:
                print(f"警告: 未找到 {self.api_key_env} 环境变量")
                print("建议配置 Etherscan V2 API 密钥以访问 50+ 条链")
        else:
            # V1 API 使用链特定的 API 密钥
            env_var = self.chain_configs[chain_id]["api_key_env"]
            api_key = os.getenv(env_var)
            if not api_key and self.verbose:
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
        
        if self.use_v2_api:
            # V2 API 需要 chainid 参数
            params["chainid"] = chain_id
            api_url = self.api_url
        else:
            # V1 API 使用链特定的 URL
            api_url = config["api_url"]
        
        if api_key:
            params["apikey"] = api_key
        
        if block_number:
            params["tag"] = block_number
        
        try:
            api_version = "V2" if self.use_v2_api else "V1"
            print(f"正在从 {config['name']} 网络获取合约源代码... (使用 Etherscan {api_version} API)")
            print(f"合约地址: {contract_address}")
            if block_number:
                print(f"区块号: {block_number}")
            
            response = requests.get(api_url, params=params, timeout=30)
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
    
    def save_contract_files(self, chain_id: str, contract_address: str, contract_data: Dict, block_number: Optional[str] = None, custom_name: Optional[str] = None) -> bool:
        """保存合约文件到本地"""
        try:
            chain_name = self.chain_configs[chain_id]["name"]
            contract_name = contract_data.get("ContractName", "Unknown")
            
            # 创建目录结构
            if custom_name:
                # 使用自定义名称作为目录名
                dir_name = custom_name
            else:
                # 使用原来的命名方式
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
    
    def download_contract(self, chain_id: str, contract_address: str, block_number: Optional[str] = None, show_header: bool = True, custom_name: Optional[str] = None) -> bool:
        """下载合约的主要方法"""
        if show_header:
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
        success = self.save_contract_files(chain_id, contract_address, contract_data, block_number, custom_name)
        
        if success:
            print(f"\n✅ 合约下载完成!")
            return True
        else:
            print(f"\n❌ 合约下载失败!")
            return False
    
    def download_contracts_batch(self, contracts: List[Dict]) -> Dict[str, bool]:
        """批量下载合约
        
        Args:
            contracts: 合约信息列表，每个元素包含:
                - name: 合约名称 (可选)
                - chain: 链标识 (如 'bsc', 'eth', 'polygon' 或链ID)
                - address: 合约地址
                - height/block: 区块高度 (可选)
        
        Returns:
            Dict: 下载结果，键为合约标识，值为是否成功
        """
        print("=" * 60)
        print("批量智能合约源代码下载器")
        print("=" * 60)
        
        # 链名称映射到ID
        chain_name_to_id = {
            'eth': '1',
            'ethereum': '1',
            'bsc': '56',
            'bnb': '56',
            'polygon': '137',
            'matic': '137',
            'fantom': '250',
            'ftm': '250',
            'avalanche': '43114',
            'avax': '43114',
            'arbitrum': '42161',
            'arb': '42161',
            'optimism': '10',
            'opt': '10'
        }
        
        results = {}
        total_contracts = len(contracts)
        successful_downloads = 0
        
        print(f"准备下载 {total_contracts} 个合约...\n")
        
        for i, contract in enumerate(contracts, 1):
            try:
                # 提取合约信息
                name = contract.get('name', f'Contract_{i}')
                chain = str(contract.get('chain', ''))
                address = contract.get('address', '')
                
                # 处理区块号 (height 或 block)
                block_number = contract.get('height') or contract.get('block')
                if block_number:
                    block_number = str(block_number)
                
                # 转换链名称为ID
                if chain.lower() in chain_name_to_id:
                    chain_id = chain_name_to_id[chain.lower()]
                else:
                    chain_id = chain
                
                print(f"\n[{i}/{total_contracts}] 正在下载: {name}")
                print(f"  链: {chain} (ID: {chain_id})")
                print(f"  地址: {address}")
                if block_number:
                    print(f"  区块: {block_number}")
                
                # 验证必要参数
                if not address:
                    print(f"❌ 错误: 合约地址为空")
                    results[f"{name}_{address}"] = False
                    continue
                
                if not chain_id or chain_id not in self.chain_configs:
                    print(f"❌ 错误: 不支持的链 '{chain}'")
                    results[f"{name}_{address}"] = False
                    continue
                
                # 下载合约
                success = self.download_contract(chain_id, address, block_number, show_header=False, custom_name=name)
                results[f"{name}_{address}"] = success
                
                if success:
                    successful_downloads += 1
                
                # 添加延迟避免API限制
                if i < total_contracts:
                    time.sleep(self.download_delay)
                    
            except Exception as e:
                print(f"❌ 处理合约时出错: {e}")
                results[f"Contract_{i}_{contract.get('address', 'unknown')}"] = False
        
        # 显示总结
        print("\n" + "=" * 60)
        print("批量下载完成!")
        print(f"成功: {successful_downloads}/{total_contracts}")
        print("=" * 60)
        
        # 显示详细结果
        print("\n详细结果:")
        for contract_id, success in results.items():
            status = "✅ 成功" if success else "❌ 失败"
            print(f"  {contract_id}: {status}")
        
        return results

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智能合约源代码下载器")
    parser.add_argument("contract_address", nargs="?", help="合约地址")
    parser.add_argument("chain_id", nargs="?", help="链ID (1=Ethereum, 56=BSC, 137=Polygon, 等)")
    parser.add_argument("--block", "-b", help="区块号 (可选)", default=None)
    parser.add_argument("--list-chains", "-l", action="store_true", help="显示支持的链")
    parser.add_argument("--batch", help="批量下载，指定包含合约信息的JSON或CSV文件路径")
    
    args = parser.parse_args()
    
    downloader = ContractDownloader()
    
    if args.list_chains:
        print("支持的区块链网络:")
        for chain_id, config in downloader.chain_configs.items():
            print(f"  {chain_id}: {config['name']} ({config['explorer_url']})")
        return
    
    if args.batch:
        # 批量下载模式
        try:
            batch_file = Path(args.batch)
            
            if not batch_file.exists():
                print(f"错误: 文件 '{args.batch}' 不存在")
                sys.exit(1)
            
            # 根据文件扩展名判断格式
            file_ext = batch_file.suffix.lower()
            
            if file_ext == '.json':
                # JSON 文件
                with open(batch_file, 'r', encoding='utf-8') as f:
                    contracts = json.load(f)
                
                if not isinstance(contracts, list):
                    print("错误: JSON文件应包含合约信息数组")
                    sys.exit(1)
                    
            elif file_ext == '.csv':
                # CSV 文件
                contracts = []
                
                with open(batch_file, 'r', encoding='utf-8') as f:
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
                            elif key_lower in ['address', 'contract_address', 'contract', '地址', '合约地址']:
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
                    sys.exit(1)
                    
            else:
                print(f"错误: 不支持的文件格式 '{file_ext}'")
                print("支持的格式: .json, .csv")
                sys.exit(1)
            
            # 执行批量下载
            results = downloader.download_contracts_batch(contracts)
            
            # 检查是否有失败的下载
            failed_count = sum(1 for success in results.values() if not success)
            if failed_count > 0:
                sys.exit(1)
                
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    else:
        # 单个合约下载模式
        if not args.contract_address or not args.chain_id:
            print("错误: 请提供合约地址和链ID，或使用 --batch 选项进行批量下载")
            parser.print_help()
            sys.exit(1)
        
        # 下载合约
        success = downloader.download_contract(args.chain_id, args.contract_address, args.block)
        
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()
