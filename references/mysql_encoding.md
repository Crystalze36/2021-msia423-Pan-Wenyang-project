```sql
SELECT default_character_set_name FROM information_schema.SCHEMATA 
WHERE schema_name = "msia423_pokemons";
```

```sql
ALTER DATABASE `msia423_pokemons` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```

```sql
ALTER TABLE msia423_pokemons.pokemons CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```

