class BundleGenerator:
    def generate_bundle(self, niche):
        # Example revenue-first assets
        bundle = {
            "ebook": f"The Complete Guide to {niche['name']}",
            "workbook": f"{niche['name']} Action Workbook",
            "checklist": f"{niche['name']} Launch Checklist",
            "prompt_pack": f"High-Converting {niche['name']} Prompt Pack"
        }
        print("Generating asset bundle...")
        for k, v in bundle.items():
            print(f" • {k}: {v}")
        return bundle
