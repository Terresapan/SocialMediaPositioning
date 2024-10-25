EVALUATE_PROMPT = """
Objective: Your task is to analyze the provided input to determine whether the core value, target audience, persona, and product/services/overall monetization strategy are logically aligned.

Input Data:
1. Core Value: {core_value_provided} - The primary value or benefit the business/service offers.
2. Target Audience: {target_audience} - The specific group of people the business is targeting.
3. Persona: {persona} - The public-facing image or identity the business/brand adopts, including tone and style.
4. Monetization Strategy: {monetization} - The products or services sold or the strategy for generating revenue.

Task:
1. Evaluate whether the core value, target audience, persona, and monetization strategy are aligned and support each other.
   - Core Value should serve the Target Audience; 
   - Persona should appeal to the Target Audience; 
   - Monetization Strategy should deliver the Core Value;
   - Persona should support the Monetization Strategy;
2. If all elements are coherent and complementary, output YES.
3. If any element appears inconsistent or contradictory, output NO.

Please provide a detailed analysis before stating your conclusion.

Example 1:
Input:
1. Core Value: Eco-friendly, sustainable beauty products that promote natural beauty and wellness.
2. Target Audience: Environmentally conscious women aged 25-40.
3. Persona: A nature-loving, wellness advocate who values sustainability and self-care.
4. Product/Monetization Strategy: Organic skincare line and eco-friendly beauty workshops.
Analysis: The core value of sustainable beauty aligns perfectly with the eco-conscious target audience. The nature-loving persona reinforces the brand message, while the organic product line and workshops provide appropriate monetization channels that match both the value proposition and audience needs.
Output: YES

Example 2:
Input:
1. Core Value: Cutting-edge AI tools for enterprise-level business automation.
2. Target Audience: Small local business owners who are just beginning to use technology.
3. Persona: An authoritative, highly technical AI expert specializing in complex systems.
4. Product/Monetization Strategy: Sophisticated AI platforms with advanced analytics, priced for large enterprises.
Analysis: There is a misalignment between the core value and the target audience. The persona of a highly technical AI expert specializing in complex systems does not align with small business owners who are new to technology
Output: NO
"""

ANALYSIS_PROMPT = """
Objective: Analyze why the elements are aligned and provide a refined, professional version of the business positioning.

Input Data:
1. Core Value: {core_value_provided}
2. Target Audience: {target_audience}
3. Persona: {persona}
4. Monetization Strategy: {monetization}
5. Alignment Status: {aligned}

Task:
1. Explain how each element supports and reinforces the others:
   - How the core value serves the target audience
   - How the persona appeals to the target audience
   - How the monetization strategy delivers the core value
   - How the persona supports the monetization strategy

2. Provide a refined version that enhances professionalism while maintaining alignment:
   - More precise core value statement
   - More detailed target audience description
   - Enhanced persona description
   - Optimized monetization strategy

Please structure your response with clear sections for the analysis and refinements.
"""

POSITIONING_PROMPT = """
Objective: Analyze the misalignment in the current positioning and provide alternative aligned combinations.

Input Data:
1. Core Value: {core_value_provided}
2. Target Audience: {target_audience}
3. Persona: {persona}
4. Monetization Strategy: {monetization}
5. Alignment Status: {aligned}

Task:
1. Identify specific points of misalignment between the elements:
   - Which elements conflict?
   - Why are they inconsistent?
   - What makes them ineffective together?

2. Provide five alternative combinations where all elements align properly:
   - Each combination should include:
     * Core Value
     * Target Audience
     * Persona
     * Monetization Strategy
   - Explain why each combination works well together

Please be specific and detailed in your analysis and suggestions.
"""