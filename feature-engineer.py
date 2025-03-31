import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def engineer_features(df):
    """Adds cybersecurity-specific features with column safety checks"""
    
    # Create copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # 1. Time-based features (always available)
    df['packets_per_second'] = (df['spkts'] + df['dpkts']) / (df['dur'].replace(0, 0.001) + 0.001)
    df['bytes_per_packet'] = (df['sbytes'] + df['dbytes']) / (df['spkts'] + df['dpkts'] + 1)
    
    # 2. Protocol-specific features (conditional)
    if all(col in df.columns for col in ['ct_http', 'ct_flw_http_mthd']):
        df['http_ratio'] = df['ct_http'] / (df['ct_flw_http_mthd'] + 1)
    else:
        print("⚠️  HTTP features not available - skipping")
    
    # 3. Behavioral features (conditional)
    if 'srcip' in df.columns:
        df['srcip_freq'] = df.groupby('srcip')['srcip'].transform('count')
    else:
        print("⚠️  srcip column not available - skipping")
    
    # 4. Normalize numerical features
    num_cols = ['dur', 'sbytes', 'dbytes', 'packets_per_second', 'bytes_per_packet']
    num_cols = [col for col in num_cols if col in df.columns]  # Filter available columns
    
    if num_cols:
        scaler = MinMaxScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])
    else:
        scaler = None
        print("⚠️  No numerical features available for scaling")
    
    return df, scaler

if __name__ == "__main__":
    try:
        # Load your cleaned data
        input_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_combined_cleaned.csv"
        output_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_engineered.csv"
        
        print("🔧 Starting feature engineering...")
        df = pd.read_csv(input_path)
        
        # Engineer features
        engineered_df, scaler = engineer_features(df)
        
        # Save results
        engineered_df.to_csv(output_path, index=False)
        print(f"✅ Saved engineered features to {output_path}")
        print("\nNew features added:")
        print([col for col in engineered_df.columns if col not in df.columns])
        
    except Exception as e:
        print(f"❌ Error during feature engineering: {str(e)}")