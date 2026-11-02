CREATE OR REPLACE PROCEDURE renombrar_ruta(p_id_ruta TEXT, p_nuevo_nombre TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_nuevo_nombre IS NULL OR btrim(p_nuevo_nombre) = '' THEN
        RAISE EXCEPTION 'El nuevo nombre no puede estar vacío';
    END IF;

    UPDATE ruta
       SET nombre = btrim(p_nuevo_nombre)
     WHERE id_ruta = p_id_ruta;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'La ruta % no existe', p_id_ruta;
    END IF;
END;
$$;