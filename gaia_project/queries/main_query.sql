WITH star_stats AS (
    SELECT 
        source_id,
        ra,
        dec,
        phot_g_mean_mag AS brightness,        
        (1000.0 / NULLIF(parallax, 0)) AS distance_pc,
        'Gaia-DR3-' || CAST(source_id AS VARCHAR) as full_name
    FROM gaia_main
    WHERE parallax > 0
)

SELECT 
    s.*,
    p.teff_gspphot AS temperature,
    v.radial_velocity,
    AVG(p.teff_gspphot) OVER() as avg_temp_total,
    RANK() OVER (ORDER BY s.brightness ASC) as brightness_rank
FROM star_stats s
LEFT JOIN gaia_params p ON s.source_id = p.source_id
LEFT JOIN gaia_variability v ON s.source_id = v.source_id;