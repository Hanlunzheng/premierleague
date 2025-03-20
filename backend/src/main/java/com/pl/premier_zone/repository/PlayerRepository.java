package com.pl.premier_zone.repository;

import com.pl.premier_zone.model.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface PlayerRepository extends JpaRepository<Player, String> {
    void deleteByName(String playerName);
    Optional<Player> findByName(String name);
    List<Player> findByTeam(String team);
    List<Player> findByPos(String position);
    List<Player> findByNationContainingIgnoreCase(String nation);
    List<Player> findByTeamAndPos(String team, String position);
} 