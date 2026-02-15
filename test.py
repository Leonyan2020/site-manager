"""
站点管理器功能测试脚本
"""
import json
from pathlib import Path


def test_config_files():
    """测试配置文件是否可以正常读写"""
    print("测试配置文件...")

    # 测试站点配置
    sites_config = Path("sites_config.json")
    if sites_config.exists():
        try:
            with open(sites_config, 'r', encoding='utf-8') as f:
                sites = json.load(f)
            print(f"[OK] 站点配置文件正常，包含 {len(sites)} 个站点")
        except Exception as e:
            print(f"[FAIL] 站点配置文件读取失败: {e}")
    else:
        print("[INFO] 站点配置文件不存在（首次运行时正常）")

    # 测试部署记录
    deployments_config = Path("deployments.json")
    if deployments_config.exists():
        try:
            with open(deployments_config, 'r', encoding='utf-8') as f:
                deployments = json.load(f)
            print(f"[OK] 部署记录文件正常，包含 {len(deployments)} 条记录")
        except Exception as e:
            print(f"[FAIL] 部署记录文件读取失败: {e}")
    else:
        print("[INFO] 部署记录文件不存在（首次运行时正常）")


def test_example_files():
    """测试示例文件"""
    print("\n测试示例文件...")

    # 测试站点配置示例
    sites_example = Path("sites_config.example.json")
    if sites_example.exists():
        try:
            with open(sites_example, 'r', encoding='utf-8') as f:
                sites = json.load(f)
            print(f"[OK] 站点配置示例文件正常，包含 {len(sites)} 个示例")
        except Exception as e:
            print(f"[FAIL] 站点配置示例文件读取失败: {e}")
    else:
        print("[FAIL] 站点配置示例文件不存在")

    # 测试部署记录示例
    deployments_example = Path("deployments.example.json")
    if deployments_example.exists():
        try:
            with open(deployments_example, 'r', encoding='utf-8') as f:
                deployments = json.load(f)
            print(f"[OK] 部署记录示例文件正常，包含 {len(deployments)} 个示例")
        except Exception as e:
            print(f"[FAIL] 部署记录示例文件读取失败: {e}")
    else:
        print("[FAIL] 部署记录示例文件不存在")


def test_imports():
    """测试模块导入"""
    print("\n测试模块导入...")

    try:
        import main
        print("[OK] main 模块导入成功")

        # 检查关键类是否存在
        if hasattr(main, 'SiteManager'):
            print("[OK] SiteManager 类存在")
        else:
            print("[FAIL] SiteManager 类不存在")

        if hasattr(main, 'SiteDialog'):
            print("[OK] SiteDialog 类存在")
        else:
            print("[FAIL] SiteDialog 类不存在")

        if hasattr(main, 'DeploymentDialog'):
            print("[OK] DeploymentDialog 类存在")
        else:
            print("[FAIL] DeploymentDialog 类不存在")

        if hasattr(main, 'MODERN_STYLE'):
            print("[OK] MODERN_STYLE 样式定义存在")
        else:
            print("[FAIL] MODERN_STYLE 样式定义不存在")

    except Exception as e:
        print(f"[FAIL] 模块导入失败: {e}")


def main():
    print("=" * 50)
    print("站点管理器 v2.0 - 功能测试")
    print("=" * 50)

    test_config_files()
    test_example_files()
    test_imports()

    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
