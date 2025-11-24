import json
from datetime import datetime, UTC
from collections import defaultdict

def format_duration(months):
    """Convert months to readable format"""
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''}"
    
    years = months // 12
    remaining_months = months % 12
    
    if remaining_months == 0:
        return f"{years} year{'s' if years != 1 else ''}"
    else:
        return f"{years} year{'s' if years != 1 else ''} {remaining_months} month{'s' if remaining_months != 1 else ''}"

def get_realistic_experience():
    """Return realistic experience data based on actual work/projects"""
    
    # Define exact experience based on your actual work
    experience_data = {
        "Programming Languages": {
            "Python": {
                "months": 1 + 4 + 3 + 2,  # Neucom(1) + TTM(4) + FPGA Orderbook(3) + LPC Filter(2) = 10 months
                "sources": [
                    "Neucom AI (1 month)",
                    "TTM Technologies (4 months)", 
                    "Real-Time Orderbook Analysis (3 months)",
                    "LPC-Based Stock Prediction (2 months)"
                ]
            },
            "Verilog/SystemVerilog": {
                "months": 8 + 8 + 3,  # Qynosys(8) + Microchip(8) + FPGA Orderbook(3) = 19 months
                "sources": [
                    "Qynosys, Inc. (8 months)",
                    "Microchip Technology (8 months)",
                    "Real-Time Orderbook Analysis (3 months)"
                ]
            },
            "C++": {
                "months": 8 + 3 + 2 + 2,  # Qynosys(8) + FPGA Orderbook(3) + Embedded Sentry(2) + Hydroponic(2) = 15 months
                "sources": [
                    "Qynosys, Inc. (8 months)",
                    "Real-Time Orderbook Analysis (3 months)",
                    "Embedded Sentry (2 months)",
                    "Hydroponic Control System (2 months)"
                ]
            },
            "C#": {
                "months": 1,  # Parallax(1)
                "sources": [
                    "Parallax AV Design (1 month)"
                ]
            },
            "VHDL": {
                "months": 1,  # Vending Machine(1)
                "sources": [
                    "Vending Machine Controller (1 month)"
                ]
            }
        },
        "Engineering Areas": {
            "Systems Programming": {
                "months": 8 + 4 + 3,  # Qynosys(8) + TTM(4) + FPGA Orderbook(3) = 15 months
                "sources": [
                    "Qynosys EW Systems (8 months)",
                    "TTM Technologies (4 months)", 
                    "Real-Time Orderbook Analysis (3 months)"
                ]
            },
            "Research Engineering": {
                "months": 1 + 9 + 3 + 2,  # Neucom(1) + NYU VIP(9) + FPGA Orderbook(3) + LPC Filter(2) = 15 months
                "sources": [
                    "NYU Processor Design Team (9 months)",
                    "Real-Time Orderbook Analysis (3 months)",
                    "LPC-Based Stock Prediction (2 months)",
                    "Neucom AI (1 month)"
                ]
            },
            "Embedded Systems": {
                "months": 8 + 2 + 2,  # Microchip(8) + Embedded Sentry(2) + Hydroponic(2) = 12 months
                "sources": [
                    "Microchip Technology (8 months)",
                    "Embedded Sentry (2 months)",
                    "Hydroponic Control System (2 months)"
                ]
            },
            "Electrical Engineering": {
                "months": 8 + 3,  # Microchip(8) + Rio Tinto(3) = 11 months
                "sources": [
                    "Microchip Technology (8 months)",
                    "Rio Tinto (3 months)"
                ]
            },
            "Financial Technology": {
                "months": 3 + 2,  # FPGA Orderbook(3) + LPC Filter(2) = 5 months
                "sources": [
                    "Real-Time Orderbook Analysis (3 months)",
                    "LPC-Based Stock Prediction (2 months)"
                ]
            },
            "Machine Learning/AI": {
                "months": 1 + 3 + 2,  # Neucom(1) + FPGA Orderbook(3) + LPC Filter(2) = 6 months
                "sources": [
                    "Neucom AI (1 month)",
                    "Real-Time Orderbook Analysis (3 months)",
                    "LPC-Based Stock Prediction (2 months)"
                ]
            }
        }
    }
    
    return experience_data

def generate_experience_trackers():
    """Generate the experience trackers section with realistic data"""
    experience_data = get_realistic_experience()
    
    experience_trackers = []
    
    for category, experiences in experience_data.items():
        category_data = {
            "category": category,
            "experiences": []
        }
        
        # Sort by total months (descending)
        sorted_experiences = sorted(experiences.items(), 
                                  key=lambda x: x[1]["months"], 
                                  reverse=True)
        
        for name, data in sorted_experiences:
            if data["months"] > 0:
                category_data["experiences"].append({
                    "name": name,
                    "total_months": data["months"],
                    "display": format_duration(data["months"]),
                    "sources": data["sources"][:3]  # Limit to top 3 sources
                })
        
        if category_data["experiences"]:
            experience_trackers.append(category_data)
    
    return experience_trackers

def convert_to_skills_format(experience_trackers):
    """Convert experience trackers to the skills format - just show time, no levels"""
    skills = []
    seen_names = set()
    
    for category in experience_trackers:
        for exp in category["experiences"]:
            # Skip duplicates and limit total skills
            if exp["name"] in seen_names or len(skills) >= 12:
                continue
            
            # Skip if less than 1 month
            if exp["total_months"] < 1:
                continue
                
            # Convert months to a 0-100 scale for the progress bar
            proficiency = min(100, max(10, exp["total_months"] * 4))  # 25 months = 100%
            
            skills.append({
                "name": exp["name"],
                "proficiency": proficiency,
                "proficiency_label": exp['display']  # Just show time, no levels
            })
            
            seen_names.add(exp["name"])
    
    # Sort by months (highest first)
    skills.sort(key=lambda x: x["proficiency"], reverse=True)
    
    return skills

def main():
    """Main function to update portfolio with realistic calculated experience"""
    # Load portfolio data
    with open("portfolio.json", "r", encoding="utf-8") as f:
        portfolio_data = json.load(f)
    
    # Generate experience trackers with realistic data
    experience_trackers = generate_experience_trackers()
    
    # Convert to skills format for template compatibility
    skills_format = convert_to_skills_format(experience_trackers)
    
    # Update portfolio data
    portfolio_data["experience_trackers"] = experience_trackers
    portfolio_data["skills"] = skills_format
    
    # Save updated portfolio
    with open("portfolio.json", "w", encoding="utf-8") as f:
        json.dump(portfolio_data, f, indent=2, ensure_ascii=False)
    
    print("Realistic experience trackers calculated and updated!")
    print("Based on actual work and project durations")
    
    # Print summary
    print("\n=== REALISTIC EXPERIENCE SUMMARY ===")
    for category in experience_trackers:
        print(f"\n{category['category']}:")
        for exp in category["experiences"]:
            print(f"  • {exp['name']}: {exp['display']}")
            print(f"    Sources: {', '.join(exp['sources'][:2])}")
    
    print(f"\n=== SKILLS DISPLAY (Accurate Time) ===")
    for skill in skills_format:
        print(f"  • {skill['name']}: {skill['proficiency_label']}")

if __name__ == "__main__":
    main()
